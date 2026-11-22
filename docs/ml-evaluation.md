# Machine learning evaluation — BrainScan AI

This repository contains an **educational computer-vision baseline**. The public site shows synthetic examples and illustrative metrics, **not actual MRI inference**. The script below can train SVM and Random Forest models only after a suitable licensed, labeled dataset is supplied locally. No clinical performance is claimed.

## Input data

Store appropriately licensed, de-identified images outside Git:

```text
dataset/
  class_a/
    img_001.png
  class_b/
    img_002.png
```

For datasets containing multiple images per patient, prepare a local CSV manifest:

```csv
path,patient_id
class_a/img_001.png,subject_001
class_b/img_002.png,subject_002
```

Paths must be relative to the dataset root. **Never commit the manifest if patient identifiers are sensitive.** Use pseudonymous IDs, and ensure different images from the same patient share an ID.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r ml/requirements.txt
python ml/train.py --data-dir dataset --groups-csv groups.csv --seed 42 --output-dir ml/artifacts
```

Omitting `--groups-csv` uses an image-level stratified split; this is **not acceptable for multi-image-per-patient medical datasets**, because subjects can leak between train and test. The script refuses to produce results when the split fails to include all classes in both partitions.

## Outputs and interpretation

The script writes `metrics.json`, `svm.joblib`, and `random_forest.joblib`. The report includes:
- Dataset file count, split method, seed, train/test sizes, and a filename-list fingerprint (not a data checksum).
- Accuracy, balanced accuracy, macro F1, per-class precision/recall/F1, and confusion matrices.
- An explicit research-only warning.

The group holdout separates known patient IDs, **but it is not an independent external validation**. Check data provenance, duplicate scans, class balance, acquisition-site leakage, calibration, uncertainty, and generalization before interpreting any results. Never infer diagnostic accuracy from the UI.

Run lightweight tests without medical images:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Do not load untrusted joblib artifacts. Models are never automatically connected to the public website.
