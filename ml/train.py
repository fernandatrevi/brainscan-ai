"""Train educational image classifiers from a local, licensed dataset.

Expected: data_dir/class_name/image.jpg. This script never downloads patient data.
A subject-level split is needed before using multi-image-per-patient datasets.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
from PIL import Image
from skimage.feature import hog
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
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
    xs, ys = [], []
    for label, folder in enumerate(classes):
        for path in sorted(folder.rglob("*")):
            if path.suffix.lower() not in EXTENSIONS:
                continue
            try:
                xs.append(features(path))
                ys.append(label)
            except (OSError, ValueError) as exc:
                print(f"Skipping unreadable image {path}: {exc}")
    if not xs:
        raise ValueError("No readable images found.")
    counts = np.bincount(ys, minlength=len(classes))
    if np.any(counts < 2):
        raise ValueError("Every class must contain at least two readable images.")
    return np.stack(xs), np.asarray(ys), [p.name for p in classes]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("ml/artifacts"))
    parser.add_argument("--test-size", type=float, default=0.2)
    args = parser.parse_args()
    if not args.data_dir.is_dir():
        parser.error("The dataset directory does not exist.")
    if not 0.05 <= args.test_size <= 0.5:
        parser.error("--test-size must be between 0.05 and 0.5")
    x, y, classes = load_dataset(args.data_dir)
    try:
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=args.test_size, random_state=42, stratify=y)
    except ValueError as exc:
        parser.error(f"Not enough images for a stratified split: {exc}")
    models = {
        "svm": make_pipeline(StandardScaler(), SVC(kernel="rbf", probability=True, random_state=42)),
        "random_forest": RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1),
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary = {"classes": classes, "n_train": len(y_train), "n_test": len(y_test),
               "warning": "Research demonstration only; image-level split may leak patients.",
               "models": {}}
    for name, model in models.items():
        model.fit(x_train, y_train)
        pred = model.predict(x_test)
        summary["models"][name] = {
            "accuracy": float(accuracy_score(y_test, pred)),
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
