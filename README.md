# BrainScan AI 🧠

**Interactive machine-learning laboratory for exploring medical-imaging classification concepts.**

[View the source code](https://github.com/fernandatrevi/brainscan-ai) · [Deployment instructions](docs/deployment.md) · [Model evaluation plan](docs/model-evaluation.md)

> **Educational prototype — not a medical device.** The live dashboard currently uses **synthetic signal samples, preconfigured confidence values, and illustrative model metrics**. It does **not** analyze MRI images, run trained predictions, or provide diagnoses.

## What is this project?

BrainScan AI is a responsive web application designed to demonstrate how a medical-imaging analytics platform might present information. It combines an interactive interface with a separate Python training pipeline that can be run **locally** when an appropriately licensed, labeled image dataset becomes available.

The goal is to practice frontend development, data preparation, supervised classification, model comparison, and responsible communication of machine-learning results.

## Current web experience

- **Interactive workspace:** switch between three synthetic samples and inspect an illustrative signal chart.
- **Mock result:** show or hide a predefined example label and confidence bar. **These are not predictions.**
- **Model explorer:** compare *illustrative*, not measured, accuracy, recall, and F1 scores for SVM, Random Forest, and an ensemble.
- **Local image picker:** choose a file to display its name. The file is **not uploaded, stored, or analyzed**.
- **Responsive interface:** dark dashboard with navigation, visualizations, and mobile-friendly layout.

## Technology stack

| Area | Technologies |
| --- | --- |
| Frontend | Next.js, React, TypeScript |
| UI | Tailwind CSS, Lucide icons |
| Charts | Recharts and SVG |
| Hosting | Vercel |
| Version control | Git and GitHub |
| Local ML experiment | Python, scikit-learn, scikit-image, NumPy, Pillow |

## Run the website locally

Requirements: a recent Node.js LTS version and npm.

```bash
git clone https://github.com/fernandatrevi/brainscan-ai.git
cd brainscan-ai
npm install
npm run dev
```

Open **http://localhost:3000**.

For a production build:

```bash
npm run build
npm run start
```

The web demo does not require API keys or environment variables.

## Train classical ML baselines (optional)

The repository also contains `ml/train.py`, a **separate** Python script for training a support vector machine (SVM) and a Random Forest using HOG features from labeled images.

Prepare a local dataset with one folder per class:

```text
dataset/
  class_a/
    image_001.png
  class_b/
    image_002.png
```

Install dependencies and run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r ml/requirements.txt
python ml/train.py --data-dir dataset --output-dir ml/artifacts
```

On Windows, activate with `.venv\Scripts\activate` instead.

The script produces trained model files and `metrics.json` containing accuracy, per-class evaluation, and confusion matrices. **No training has been executed as part of this README update, and no measured results are claimed here.** These artifacts are not connected to the deployed website.

**Evaluation caution:** the example script uses an image-level stratified split. If a dataset contains multiple images from the same patient, a **patient-level/group split** is required to prevent leakage. Dataset licenses, class imbalance, data quality, calibration, and external generalization must be reviewed before reporting meaningful performance.

For additional detail, read [ml/README.md](ml/README.md) and [docs/model-evaluation.md](docs/model-evaluation.md).

## Project structure

```text
app/             Next.js routes, layout and styles
components/      Interactive dashboard UI and charts
lib/             Types, formatting and synthetic demo data
ml/              Optional local training script and requirements
docs/            Deployment, roadmap, privacy and evaluation notes
package.json     Frontend dependencies and scripts
vercel.json      Vercel framework configuration
```

## Deployment

The website is configured for **Vercel**. To deploy your own copy:

1. Import this GitHub repository into Vercel.
2. Use the **Next.js** framework preset and repository root (`./`).
3. Select **Deploy**.
4. Verify the dashboard interactions at your assigned `*.vercel.app` address.

See [docs/deployment.md](docs/deployment.md). The precise production URL is intentionally not listed here because it has not been confirmed.

## Roadmap

- [x] Create a responsive, interactive dashboard.
- [x] Add synthetic sample selection and signal visualization.
- [x] Show illustrative model comparisons and a local-only file picker.
- [x] Add a separate SVM/Random Forest training script.
- [ ] Select and audit a public, appropriately licensed imaging dataset.
- [ ] Train and evaluate models using leakage-safe data splits.
- [ ] Replace illustrative metrics with documented experimental results.
- [ ] Evaluate deployment options for secure, validated inference.
- [ ] Integrate real predictions only after testing, privacy review, and clear limitations.

## Privacy and limitations

This project is for **learning and portfolio demonstration**. Do not upload or commit patient images, identifying medical data, private credentials, or trained model artifacts. The current frontend does not process medical images. No clinical interpretation or medical recommendation should be based on this application.

See [docs/privacy.md](docs/privacy.md).

## Author

Developed in the [fernandatrevi](https://github.com/fernandatrevi) GitHub portfolio.
