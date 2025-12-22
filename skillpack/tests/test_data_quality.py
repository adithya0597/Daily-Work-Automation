"""Tests for data_quality skill."""

from pathlib import Path

import pytest

from skillpack.skills.data_quality import (
    generate_data_quality,
    generate_example_config,
    generate_pandera_schema,
)


def test_generate_example_config_has_required_fields() -> None:
    """Test that example config has required fields."""
    config = generate_example_config()
    assert "name" in config
    assert "columns" in config
    assert len(config["columns"]) > 0


def test_generate_pandera_schema_creates_python() -> None:
    """Test that schema generation creates valid Python code."""
    config = generate_example_config()
    schema_code = generate_pandera_schema(config)

    assert "import pandera" in schema_code
    assert "DataFrameSchema" in schema_code
    assert config["name"] in schema_code


def test_generate_data_quality_creates_files(tmp_path: Path) -> None:
    """Test that generate_data_quality creates output files."""
    schema_path, runner_path = generate_data_quality(
        config_path=None,  # Use example config
        base_dir=str(tmp_path / "out"),
    )

    assert schema_path.exists()
    assert runner_path.exists()
    assert schema_path.name == "schema.py"
    assert runner_path.name == "run_validation.py"


def test_generate_data_quality_from_config(tmp_path: Path) -> None:
    """Test generation from a config file."""
    # Create config file
    config_path = tmp_path / "config.yaml"
    config_path.write_text("""
name: TestSchema
columns:
  - name: id
    type: integer
    nullable: false
""")

    schema_path, runner_path = generate_data_quality(
        config_path=str(config_path),
        base_dir=str(tmp_path / "out"),
    )

    schema_content = schema_path.read_text()
    assert "TestSchema" in schema_content
