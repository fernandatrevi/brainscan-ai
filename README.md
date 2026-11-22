# BrainScan AI 🧠

**Interactive machine-learning laboratory for exploring medical-imaging classification concepts.**

[**Open web demo**](https://brainscan-ai-one.vercel.app/) · [**Engineering case study**](docs/ENGINEERING_CASE_STUDY.md) · [Evaluation protocol](docs/ml-evaluation.md) · [Deployment instructions](docs/deployment.md)

> **Educational prototype — not a medical device.** The live dashboard currently uses **synthetic signal samples, preconfigured confidence values, and illustrative model metrics**. It does **not** analyze MRI images, run trained predictions, or provide diagnoses.

## What is this project?

BrainScan AI is a responsive web application designed to demonstrate how a medical-imaging analytics platform might present information. It combines an interactive interface with a separate Python training pipeline that can be run **locally** when an appropriately licensed, labeled image dataset becomes available.

The goal is to practice frontend development, data preparation, supervised classification, model comparison, and responsible communication of machine-learning results.

## Current web experience

- **Interactive workspace:** switch between three synthetic samples and inspect an illustrative signal chart.
- **Mock result:** show or hide a predefined example label and confidence bar. **These are not predictions.**
- **Model explorer:** explains the implemented reference classifier, SVM and Random Forest pipeline, evaluation metrics, and the requirements for responsible assessment—without presenting fabricated model scores.
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

## Reproducible ML experimentation (Python)

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

The pipeline compares a **majority-class reference**, **HOG + SVM**, and **HOG + Random Forest** on the same held-out partition. It records accuracy, balanced accuracy, macro F1, per-class statistics, confusion matrices, class distributions, exact-file duplicate audits, and experiment settings. The test suite also runs an end-to-end training check on **synthetic, non-medical images**.\n\n**No independently verified performance results on medical images are published, and no clinical accuracy is claimed.** The models are not connected to the public website. See the [evaluation protocol](docs/ml-evaluation.md).

**Evaluation caution:** the default image-level stratified split cannot establish patient-level separation. When patient identifiers are available, provide a pseudonymous CSV with `--groups-csv` to enforce a patient-separated split. Byte-identical duplicates across train/test or with conflicting labels cause training to stop, but this does **not** detect near duplicates or multiple scans of the same patient. Dataset licenses, class balance, calibration, and independent external generalization remain open questions.

For additional detail, read [ml/README.md](ml/README.md), [docs/ml-evaluation.md](docs/ml-evaluation.md), and [docs/model-evaluation.md](docs/model-evaluation.md). Run tests with `python -m unittest discover -s tests -p 'test_*.py' -v`.

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

See [docs/deployment.md](docs/deployment.md). Vercel lists the project at [https://brainscan-ai-one.vercel.app/](https://brainscan-ai-one.vercel.app/) (as shown in the owner's dashboard). Its public loading and interactive functions have not been independently verified.

## Roadmap

- [x] Create a responsive, interactive dashboard.
- [x] Add synthetic sample selection and signal visualization.
- [x] Show illustrative model comparisons and a local-only file picker.
- [x] Add a separate SVM/Random Forest training script.
- [ ] Select and audit a public, appropriately licensed imaging dataset.
- [x] Add group-aware splitting, exact-duplicate checks, a simple baseline, measured-metric export, and synthetic integration tests.\n- [ ] Obtain suitable patient identifiers and run independently reviewed, patient-separated medical-image evaluation.
- [x] Remove fabricated benchmark percentages from the dashboard.\n- [ ] Publish independently verified experimental measurements with documented dataset provenance.
- [ ] Evaluate deployment options for secure, validated inference.
- [ ] Integrate real predictions only after testing, privacy review, and clear limitations.

## Privacy and limitations

This project is for **learning and portfolio demonstration**. Do not upload or commit patient images, identifying medical data, private credentials, or trained model artifacts. The current frontend does not process medical images. No clinical interpretation or medical recommendation should be based on this application.

See [docs/privacy.md](docs/privacy.md).

## Author

Developed in the [fernandatrevi](https://github.com/fernandatrevi) GitHub portfolio.

## Additional project documentation

- [Release readiness checklist](docs/release-readiness-checklist.md) — verification steps, limitations, and responsible-use considerations.
