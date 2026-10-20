# Train the BrainScan AI baselines on GitHub Actions

The Kaggle MRI dataset is downloaded at runtime, **not added to the Git repository**.

1. Open [Actions](https://github.com/fernandatrevi/brainscan-ai/actions).
2. Select **Train MRI baseline models** in the left sidebar.
3. Choose **Run workflow** on the `main` branch.
4. Wait for the workflow to finish. Public dataset download and training may take several minutes.
5. Open the completed run and download the **brainscan-baseline-metrics** artifact.
6. Extract `metrics.json` to inspect the measured test-set results.

The pipeline uses only the Kaggle **Training** directory and creates a new stratified image-level split for initial experimentation. The original Kaggle Testing folder is not used. This is **not patient-disjoint validation**; near-duplicates, leakage and source bias may inflate scores. Do not claim clinical performance.

The workflow is manual to avoid unrequested downloads and compute use. It requires GitHub Actions to be enabled and enough free Actions minutes. Kaggle may change access or licensing terms; if downloading fails, review the run logs.

The website on Vercel **still uses synthetic examples and illustrative metrics**. The trained models are not deployed to the website. Do not use this project for medical decisions.
