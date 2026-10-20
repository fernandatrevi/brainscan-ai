"""Download the public Kaggle dataset and prepare a training-only class layout.

Requires kagglehub. Does not copy or commit images into the repository.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import kagglehub

SLUG = "masoudnickparvar/brain-tumor-mri-dataset"
LABELS = {"glioma", "meningioma", "notumor", "pituitary"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("dataset"))
    args = parser.parse_args()
    source = Path(kagglehub.dataset_download(SLUG))
    training = [p for p in source.rglob("Training") if p.is_dir()]
    if len(training) != 1:
        raise RuntimeError(f"Expected one Training folder, found {len(training)} under {source}")
    train_dir = training[0]
    classes = {p.name.lower(): p for p in train_dir.iterdir() if p.is_dir()}
    if set(classes) != LABELS:
        raise RuntimeError(f"Unexpected classes: {sorted(classes)}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, folder in classes.items():
        destination = args.output_dir / name
        destination.mkdir(exist_ok=True)
        count = 0
        for path in folder.iterdir():
            if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                shutil.copy2(path, destination / path.name)
                count += 1
        print(f"{name}: {count} images")
        if count < 10:
            raise RuntimeError(f"Too few images in {name}")
    print("Prepared training images only. Kaggle's Testing folder is NOT used here.")


if __name__ == "__main__":
    main()
