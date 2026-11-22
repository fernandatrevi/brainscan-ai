# BrainScan AI — Engineering case study

## Problem and scope

Medical-image machine learning requires more than a visually convincing interface. A credible experiment needs reproducible preprocessing, honest reference models, disciplined data separation, inspectable failure cases, and clear statements of where evidence stops.

BrainScan AI is an **educational engineering project**, not a medical device or diagnostic tool. Its Next.js interface is a synthetic demonstration; it does not perform real inference. A separate Python pipeline implements classical image classification that can be evaluated on locally obtained and appropriately licensed images.

## Architecture

```text
Next.js / React interface (synthetic demonstrations only)
  ├── Interactive sample exploration
  └── ML methodology and limitations
                 [NOT CONNECTED TO INFERENCE]

Local Python experiment (real training, suitable dataset required)
  ├── Class-folder image loader and grayscale resize
  ├── HOG features
  ├── Stratified image split or optional patient-group holdout
  ├── SHA-256 exact-duplicate / contradictory-label checks
  ├── Majority-class reference
  ├── StandardScaler + SVM / Random Forest
  └── JSON report (accuracy, balanced accuracy, macro F1,
                   per-class scores, confusion matrices)
```

## Engineering decisions

| Decision | Why | Remaining limitation |
|---|---|---|
| Start with HOG features and classical models | Transparent, reproducible baseline without a heavy GPU environment | Does not match modern validated medical-vision systems |
| Compare to a dummy classifier | Makes poor model performance easier to recognize under imbalance | One baseline does not establish comparative state of the art |
| Separate groups when IDs exist | Reduces same-patient train/test leakage | No patient identities are inferred from filenames |
| Reject exact cross-split duplicates and conflicting labels | Prevents one easily overlooked evaluation error | Near-duplicates, re-encodings and repeated-patient scans remain possible |
| Save per-class metrics, counts and settings | Enables examination beyond headline accuracy | No external test set or clinical calibration is established |
| Test training with generated patterns | Verifies that the CLI, saving and reporting work without distributing sensitive images | The smoke test does not measure MRI classification accuracy |
| Remove fabricated web benchmark scores | Avoids presenting illustrative numbers as measured results | Web experience remains an educational mock until separately validated |

## Verification

```bash
pip install -r ml/requirements.txt
python -m unittest discover -s tests -p "test_*.py" -v
```

The suite includes split-integrity tests, exact-duplicate checks and a CLI smoke test using generated non-medical images. GitHub Actions is configured to run these tests on relevant changes; inspect the Actions tab for live pass/fail results rather than assuming that a committed workflow has passed.

For local experiments, see [ml/README.md](../ml/README.md) and [the evaluation protocol](ml-evaluation.md).

## What is and is not demonstrated

**Implemented:** a reproducible baseline design, real fitting code, split and data-quality protections, structured metrics, model artifact generation, and an interactive educational frontend.

**Not demonstrated:** a verified medical-image accuracy score, patient-independent Kaggle validation, a calibrated diagnostic classifier, deployed medical-image inference, external generalization, or medical safety.

## Next research milestone

Source a dataset with documented license, provenance and usable patient or study identifiers; audit near-duplicate scans; fix the train/validation/test protocol before modeling; establish suitable error tolerances with domain experts; report uncertainty, calibration and per-class sensitivity; and test on an independent institution or acquisition setting. Only then consider connecting a model to a clearly non-clinical research frontend.
