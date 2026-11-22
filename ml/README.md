# Real model training (optional, local only)

The live website currently shows **synthetic examples and mock metrics**, not model predictions. This directory provides a separate, reproducible baseline that can be run once you have permission to use a labeled image dataset.

## Prepare data

Place locally acquired, appropriately licensed images in:

```text
dataset/
  class_a/
    image_001.png
  class_b/
    image_002.png
```

Do not commit the dataset, patient images, or model artifacts. Do not use identifiable clinical images.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r ml/requirements.txt
python ml/train.py --data-dir dataset --output-dir ml/artifacts
```

Windows activation: `.venv\\Scripts\\activate`.

Outputs: `metrics.json`, `svm.joblib`, and `random_forest.joblib`. Results are **not automatically connected to the Vercel frontend**.

For the patient-separated evaluation protocol and metric definitions, see [ML evaluation guide](../docs/ml-evaluation.md).

## Critical limitations

- By default the script uses an **image-level stratified split**. For multiple images per patient, pass `--groups-csv groups.csv` for a patient-separated holdout. An independent external test set is still required for generalization claims.
- HOG is a simple baseline, not a validated MRI tumor detector.
- Dataset labels, licenses, image preprocessing, class balance, and domain shift require separate review.
- Do not load untrusted `.joblib` files; serialized models can execute code.
- This project is educational and must not be used for medical decisions.
