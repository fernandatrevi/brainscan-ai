"""Data-leakage tests using synthetic file bytes, never patient images."""
from pathlib import Path

import numpy as np
import pytest

from ml.quality import audit_images


def test_duplicate_image_crossing_split_is_rejected(tmp_path: Path):
    for name, data in [("a.png", b"same"), ("b.png", b"same"), ("c.png", b"different")]:
        (tmp_path / name).write_bytes(data)
    with pytest.raises(ValueError, match="cross train/test"):
        audit_images(tmp_path, ["a.png", "b.png", "c.png"], np.array([0, 0, 1]), [0, 2], [1])


def test_duplicate_labels_conflict_is_rejected(tmp_path: Path):
    (tmp_path / "a.png").write_bytes(b"same")
    (tmp_path / "b.png").write_bytes(b"same")
    with pytest.raises(ValueError, match="contradictory labels"):
        audit_images(tmp_path, ["a.png", "b.png"], np.array([0, 1]), [0], [1])


def test_distinct_content_is_accepted(tmp_path: Path):
    for i in range(4):
        (tmp_path / f"{i}.png").write_bytes(f"image-{i}".encode())
    result = audit_images(tmp_path, [f"{i}.png" for i in range(4)],
                          np.array([0, 0, 1, 1]), [0, 2], [1, 3])
    assert result["cross_split_exact_duplicates"] == 0
    assert result["unique_image_hashes"] == 4
