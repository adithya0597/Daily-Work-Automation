"""Tests for profile_dataset skill."""

from pathlib import Path

import pytest

from skillpack.skills.profile_dataset import (
    generate_profile,
    infer_dtype,
    profile_column,
    profile_csv,
)


SAMPLE_CSV = """id,name,age,active
1,Alice,28,true
2,Bob,35,false
3,Charlie,,true
"""


@pytest.fixture
def csv_file(tmp_path: Path) -> Path:
    """Create a temporary CSV file."""
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(SAMPLE_CSV)
    return csv_path


def test_infer_dtype_integer() -> None:
    """Test integer type inference."""
    assert infer_dtype(["1", "2", "3"]) == "integer"


def test_infer_dtype_float() -> None:
    """Test float type inference."""
    assert infer_dtype(["1.5", "2.5", "3.5"]) == "float"


def test_infer_dtype_boolean() -> None:
    """Test boolean type inference."""
    assert infer_dtype(["true", "false", "true"]) == "boolean"


def test_infer_dtype_string() -> None:
    """Test string type inference."""
    assert infer_dtype(["hello", "world"]) == "string"


def test_profile_column_basic() -> None:
    """Test basic column profiling."""
    profile = profile_column("test", ["a", "b", "", "c"])
    assert profile.name == "test"
    assert profile.total_count == 4
    assert profile.null_count == 1
    assert profile.unique_count == 3


def test_profile_csv_creates_profile(csv_file: Path) -> None:
    """Test that profile_csv creates a valid profile."""
    profile = profile_csv(csv_file)
    assert profile.row_count == 3
    assert profile.column_count == 4
    assert len(profile.columns) == 4


def test_generate_profile_creates_files(csv_file: Path, tmp_path: Path) -> None:
    """Test that generate_profile creates output files."""
    md_path, json_path = generate_profile(
        csv_path=str(csv_file),
        base_dir=str(tmp_path / "out"),
    )

    assert md_path.exists()
    assert json_path.exists()
    assert md_path.suffix == ".md"
    assert json_path.suffix == ".json"
