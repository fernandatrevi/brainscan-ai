"""Dataset integrity checks for educational image-classification experiments.

Exact-byte duplicates are not a substitute for perceptual/patient-level checks.
"""
from __future__ import annotations

import hashlib
from collections import defaultdict
from pathlib import Path


def audit_images(root: Path, paths: list[str], labels, train_indices, test_indices):
    """Reject exact duplicates that could invalidate a held-out evaluation."""
    by_hash = defaultdict(list)
    for index, relative_path in enumerate(paths):
        digest = hashlib.sha256((root / relative_path).read_bytes()).hexdigest()
        by_hash[digest].append(index)
    conflicts = []
    overlapping = []
    train = set(map(int, train_indices))
    test = set(map(int, test_indices))
    for indices in by_hash.values():
        classes = {int(labels[i]) for i in indices}
        if len(classes) > 1:
            conflicts.append([paths[i] for i in indices])
        if any(i in train for i in indices) and any(i in test for i in indices):
            overlapping.append([paths[i] for i in indices])
    if conflicts:
        raise ValueError(
            f"{len(conflicts)} exact-image duplicate group(s) have contradictory labels. "
            f"Example: {conflicts[0]}"
        )
    if overlapping:
        raise ValueError(
            f"{len(overlapping)} exact-image duplicate group(s) cross train/test. "
            "Deduplicate before training or split by patient/group. "
            f"Example: {overlapping[0]}"
        )
    return {
        "sha256_duplicate_groups": sum(len(v) > 1 for v in by_hash.values()),
        "unique_image_hashes": len(by_hash),
        "cross_split_exact_duplicates": 0,
        "contradictory_label_duplicate_groups": 0,
        "caveat": "Byte-identical duplicates only; resized/re-encoded or same-patient scans may remain.",
    }
