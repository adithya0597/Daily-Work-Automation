"""Tests for dbt_generator skill."""

from pathlib import Path

import pytest

from skillpack.skills.dbt_generator import (
    generate_dbt,
    generate_schema_yml,
    generate_staging_model,
    get_example_config,
)


def test_get_example_config_has_required_fields() -> None:
    """Test that example config has required fields."""
    config = get_example_config()
    assert "project_name" in config
    assert "sources" in config
    assert "models" in config
    assert len(config["sources"]) > 0


def test_generate_staging_model_creates_sql() -> None:
    """Test staging model generation."""
    source = {
        "source_name": "raw",
        "table_name": "users",
        "columns": [
            {"name": "id", "alias": "user_id"},
            {"name": "email"},
        ],
    }

    sql = generate_staging_model(source)
    assert "{{ source('raw', 'users') }}" in sql
    assert "user_id" in sql
    assert "email" in sql


def test_generate_schema_yml_creates_valid_yaml() -> None:
    """Test schema.yml generation."""
    config = get_example_config()
    schema = generate_schema_yml(config)

    assert schema["version"] == 2
    assert "models" in schema
    assert len(schema["models"]) > 0


def test_generate_dbt_creates_directory_structure(tmp_path: Path) -> None:
    """Test that generate_dbt creates proper directory structure."""
    output_dir = generate_dbt(
        config_path=None,  # Use example config
        base_dir=str(tmp_path / "out"),
    )

    # Check directory structure
    models_dir = output_dir / "models"
    assert models_dir.exists()
    assert (models_dir / "staging").exists()
    assert (models_dir / "marts").exists()
    assert (models_dir / "schema.yml").exists()
    assert (models_dir / "docs.md").exists()


def test_generate_dbt_creates_staging_models(tmp_path: Path) -> None:
    """Test that staging models are created."""
    output_dir = generate_dbt(
        config_path=None,
        base_dir=str(tmp_path / "out"),
    )

    staging_dir = output_dir / "models" / "staging"
    staging_files = list(staging_dir.glob("*.sql"))
    assert len(staging_files) > 0

    # Check content of a staging model
    sql_content = staging_files[0].read_text()
    assert "{{ config(" in sql_content
    assert "{{ source(" in sql_content
