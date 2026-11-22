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

## Dataset integrity and comparative baseline

Before fitting either classifier, `ml/quality.py` hashes each input image file with SHA-256. The run **fails** if byte-identical files have contradictory labels or appear in both train and test. The machine-readable report records counts and makes this limited protection visible. A re-encoded copy, near duplicate, or two scans from the same person may evade exact-file hashing. **Use `--groups-csv` when patient/group IDs are available**, and separately audit any duplicated or closely related scans.

The same split is used to compare three approaches:

| Approach | Purpose |
|---|---|
| Majority-class dummy | Sanity-check reference that always predicts the most frequent class |
| HOG + scaled RBF SVM | Classical gradient-feature classifier |
| HOG + Random Forest | Tree-ensemble classifier on the same gradient features |

Class balance matters: accuracy alone can hide missed minority classes. Read balanced accuracy, macro F1, class-level precision/recall, and the confusion matrix **together**. The report records image counts per class and seed. The reported values are sample-dependent; they must not be interpreted as real-world diagnostic performance.

## Automated verification

The GitHub Actions workflow `ml-checks.yml` runs syntax checks and unit tests, including a **synthetic non-medical image training smoke test**. This demonstrates that preprocessing, model fitting, saved artifacts and metric reporting work end-to-end. It is not an imaging benchmark and does not establish clinical validity.

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

The separate `train-baselines.yml` workflow prepares a public Kaggle MRI sample and can generate an **exploratory** image-level holdout report. The dataset does not supply verified patient identifiers through this preparation script; its results must **never** be described as patient-independent validation. Audit the dataset license and provenance before use, and obtain an external patient-separated evaluation dataset before making scientific comparisons.

## Releasing results responsibly

Only promote measured results into the frontend after recording the dataset citation and license, content-based data audit, patient/group separation strategy, sample counts, evaluation script revision, full class-level metrics, known sources of leakage, and limitations. Keep source images and patient identifiers outside Git. Document calibration, uncertainty and domain-shift evaluation before considering any clinical setting.
