# Dataset selection for BrainScan AI

## Recommended starter dataset: Brain Tumor MRI Dataset (Kaggle)

- Source: https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset
- Dataset DOI: https://doi.org/10.34740/kaggle/dsv/2645886
- Curator: Masoud Nickparvar
- Reported size: 7,023 brain MRI images
- Classes: glioma, meningioma, no tumor, pituitary
- License shown on the Kaggle dataset page: CC0 (check current terms and upstream provenance before redistribution)
- Dataset is assembled from Figshare, SARTAJ, and Br35H.

**Cautions:** The dataset combines images from different sources. It may contain duplicates, source-specific artifacts, label inconsistencies, and overlapping patient data. A random image-level train/test split alone cannot establish clinical generalization. The original curator notes issues in the SARTAJ glioma labels.

## Alternative with patient identifiers: Figshare

- Original: https://figshare.com/articles/dataset/brain_tumor_dataset/1512427
- License: CC BY 4.0; attribution required
- Reported size: 3,064 T1-weighted contrast-enhanced MRI slices from 233 patients
- Classes: meningioma, glioma, pituitary (no healthy/no-tumor class)
- A converted dataset with patient identifiers and patient-disjoint folds is documented at https://huggingface.co/datasets/MedOtter/Figshare_Brain_Tumor

For rigorous evaluation, prefer patient-disjoint splits where identifiers are available. Verify any repackaged dataset against its original source.

## Suggested first experiment

1. Download the Kaggle dataset **locally**; do not commit images.
2. Inspect class counts, image dimensions, duplicates, and provenance.
3. Check whether training and testing folders have overlapping or near-duplicate images.
4. Train SVM and Random Forest HOG baselines using the existing `ml/train.py` script on a vetted folder layout.
5. Report per-class precision, recall, F1, confusion matrices, and the evaluation split's limitations.
6. Do not display real model metrics in the web UI until training and verification are completed.

The current website is a mock demonstration. No real model is deployed and no clinical use is intended.
