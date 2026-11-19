# Release readiness checklist

BrainScan AI currently demonstrates a medical-imaging **interface**, not validated MRI inference. Its example outputs and performance figures are illustrative.

## Website checks

- Run `npm install`, `npm run build`, and the available lint/test commands from a clean checkout.
- Verify layout and keyboard navigation on mobile and desktop.
- Label all synthetic inputs, preset confidence values, and illustrative metrics prominently.
- Ensure selecting an image cannot be mistaken for obtaining a medical prediction.
- Check external links and deployment behavior after changes.

## Local ML experiment checks

- Confirm that the image dataset is legally reusable and has reliable ground-truth labels.
- Split images by patient or acquisition group, not by image file alone, to prevent leakage.
- Fit any preprocessing exclusively on training partitions.
- Report class counts, confusion matrices, per-class recall, and uncertainty across splits.
- Assess external-site generalization and subgroup performance before making broader claims.
- Keep trained weights and potentially sensitive medical images out of Git unless publication is authorized.

## Non-negotiable communication

Do not call the mock dashboard a diagnostic tool, claim measured model accuracy based on preset UI figures, or imply that an uploaded image is analyzed by the live website. Any real clinical workflow would require separate verification, risk management, privacy controls, and applicable regulatory review.

This checklist documents work to verify; it does not assert that tests or training have already passed.
