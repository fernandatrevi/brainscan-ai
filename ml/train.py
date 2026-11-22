"""Train educational image classifiers from a local, licensed dataset.

Expected: data_dir/class_name/image.jpg. This script never downloads patient data.
A subject-level split is needed before using multi-image-per-patient datasets.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
from PIL import Image
from skimage.feature import hog
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def features(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        gray = np.asarray(image.convert("L").resize((128, 128)), dtype=np.float32) / 255
    return hog(gray, orientations=9, pixels_per_cell=(16, 16),
               cells_per_block=(2, 2), block_norm="L2-Hys")


def load_dataset(root: Path):
    classes = sorted(p for p in root.iterdir() if p.is_dir())
    if len(classes) < 2:
        raise ValueError("Dataset needs at least two class folders.")
    xs, ys, paths = [], [], []
    for label, folder in enumerate(classes):
        for path in sorted(folder.rglob("*")):
            if path.suffix.lower() not in EXTENSIONS:
                continue
            try:
                xs.append(features(path))
                ys.append(label)
                paths.append(path.relative_to(root).as_posix())
            except (OSError, ValueError) as exc:
                print(f"Skipping unreadable image {path}: {exc}")
    if not xs:
        raise ValueError("No readable images found.")
    counts = np.bincount(ys, minlength=len(classes))
    if np.any(counts < 2):
        raise ValueError("Every class must contain at least two readable images.")
    return np.stack(xs), np.asarray(ys), [p.name for p in classes], paths



def select_split(y, paths, test_size, seed, groups_csv=None):
    """Split without sharing a subject across train and test when groups are supplied."""
    indices = np.arange(len(y))
    if groups_csv is None:
        train, test = train_test_split(indices, test_size=test_size,
                                       random_state=seed, stratify=y)
        return train, test, "stratified_image"
    with groups_csv.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not {"path", "patient_id"}.issubset(reader.fieldnames or []):
            raise ValueError("Groups CSV requires path and patient_id columns.")
        mapping = {}
        for row in reader:
            path, patient = row["path"].strip().replace("\\", "/"), row["patient_id"].strip()
            if not path or not patient or path in mapping:
                raise ValueError("Groups CSV contains an empty or duplicate path/patient_id.")
            mapping[path] = patient
    missing = sorted(set(paths) - set(mapping))
    if missing:
        raise ValueError(f"Missing patient IDs for {len(missing)} images; first: {missing[0]}")
    groups = np.array([mapping[p] for p in paths])
    if len(set(groups)) < 2:
        raise ValueError("At least two distinct patients/groups are required.")
    splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
    train, test = next(splitter.split(indices, y, groups))
    if set(groups[train]) & set(groups[test]):
        raise RuntimeError("Patient overlap between train and test.")
    return train, test, "patient_group"


def check_split(y, train, test, n_classes):
    if set(y[train]) != set(range(n_classes)) or set(y[test]) != set(range(n_classes)):
        raise ValueError("Both train and test must contain every class. "
                         "Acquire more subjects/images or change the seed/test fraction.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("ml/artifacts"))
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--groups-csv", type=Path, help="CSV: path,patient_id relative to data-dir; prevents subject leakage")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if not args.data_dir.is_dir():
        parser.error("The dataset directory does not exist.")
    if not 0.05 <= args.test_size <= 0.5:
        parser.error("--test-size must be between 0.05 and 0.5")
    x, y, classes, paths = load_dataset(args.data_dir)
    try:
        train, test, split_type = select_split(y, paths, args.test_size, args.seed, args.groups_csv)
        check_split(y, train, test, len(classes))
    except ValueError as exc:
        parser.error(f"Dataset split invalid: {exc}")
    x_train, x_test, y_train, y_test = x[train], x[test], y[train], y[test]
    models = {
        "svm": make_pipeline(StandardScaler(), SVC(kernel="rbf", probability=True, random_state=args.seed)),
        "random_forest": RandomForestClassifier(n_estimators=300, random_state=args.seed, n_jobs=-1),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary = {"classes": classes, "n_train": len(y_train), "n_test": len(y_test),
               "seed": args.seed, "test_size": args.test_size, "split_type": split_type,
               "dataset_file_count": len(paths),
               "dataset_path_fingerprint": hashlib.sha256("\\n".join(sorted(paths)).encode()).hexdigest(),
               "warning": "Educational baseline only; no clinical validation. "
                          + ("Image-level splits can leak patient information." if split_type == "stratified_image" else "Patient-separated holdout; independent external validation is still needed."),
               "models": {}}
    for name, model in models.items():
        model.fit(x_train, y_train)
        pred = model.predict(x_test)
        summary["models"][name] = {
            "accuracy": float(accuracy_score(y_test, pred)),
            "balanced_accuracy": float(balanced_accuracy_score(y_test, pred)),
            "macro_f1": float(f1_score(y_test, pred, average="macro", zero_division=0)),
            "classification_report": classification_report(
                y_test, pred, labels=list(range(len(classes))),
                target_names=classes, zero_division=0, output_dict=True),
            "confusion_matrix": confusion_matrix(
                y_test, pred, labels=list(range(len(classes)))).tolist(),
        }
        joblib.dump({"model": model, "classes": classes}, args.output_dir / f"{name}.joblib")
    (args.output_dir / "metrics.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["models"], indent=2))


if __name__ == "__main__":
    main()
