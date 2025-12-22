"""Tests for schema_diff skill."""

import json
from pathlib import Path

import pytest

from skillpack.skills.schema_diff import (
    Column,
    diff_schema,
    diff_schemas,
    parse_schema,
)


OLD_SCHEMA = {
    "columns": [
        {"name": "id", "type": "INTEGER", "nullable": False, "pk": True},
        {"name": "email", "type": "VARCHAR(255)", "nullable": False},
    ]
}

NEW_SCHEMA = {
    "columns": [
        {"name": "id", "type": "INTEGER", "nullable": False, "pk": True},
        {"name": "email", "type": "VARCHAR(255)", "nullable": False},
        {"name": "name", "type": "VARCHAR(100)", "nullable": True},
    ]
}


@pytest.fixture
def schema_files(tmp_path: Path) -> tuple[Path, Path]:
    """Create temporary schema files."""
    old_path = tmp_path / "old.json"
    new_path = tmp_path / "new.json"
    old_path.write_text(json.dumps(OLD_SCHEMA))
    new_path.write_text(json.dumps(NEW_SCHEMA))
    return old_path, new_path


def test_parse_schema_creates_columns(schema_files: tuple[Path, Path]) -> None:
    """Test that parse_schema creates Column objects."""
    old_path, _ = schema_files
    schema = parse_schema(old_path)
    assert "id" in schema
    assert "email" in schema
    assert isinstance(schema["id"], Column)


def test_diff_schemas_detects_additions() -> None:
    """Test that diff detects added columns."""
    old = {"id": Column("id", "INTEGER", False, True)}
    new = {
        "id": Column("id", "INTEGER", False, True),
        "name": Column("name", "VARCHAR", True, False),
    }

    diff = diff_schemas(old, new)
    assert len(diff.added_columns) == 1
    assert diff.added_columns[0].name == "name"


def test_diff_schemas_detects_removals() -> None:
    """Test that diff detects removed columns."""
    old = {
        "id": Column("id", "INTEGER", False, True),
        "deleted": Column("deleted", "VARCHAR", True, False),
    }
    new = {"id": Column("id", "INTEGER", False, True)}

    diff = diff_schemas(old, new)
    assert len(diff.removed_columns) == 1
    assert diff.removed_columns[0].name == "deleted"


def test_diff_schemas_detects_modifications() -> None:
    """Test that diff detects modified columns."""
    old = {"col": Column("col", "VARCHAR(100)", True, False)}
    new = {"col": Column("col", "VARCHAR(255)", False, False)}

    diff = diff_schemas(old, new)
    assert len(diff.modified_columns) == 1


def test_diff_schema_creates_files(schema_files: tuple[Path, Path], tmp_path: Path) -> None:
    """Test that diff_schema creates output files."""
    old_path, new_path = schema_files

    sql_path, notes_path = diff_schema(
        old_path=str(old_path),
        new_path=str(new_path),
        base_dir=str(tmp_path / "out"),
    )

    assert sql_path.exists()
    assert notes_path.exists()
    assert sql_path.suffix == ".sql"
    assert notes_path.suffix == ".md"

    # Check SQL content
    sql_content = sql_path.read_text()
    assert "ALTER TABLE" in sql_content
    assert "ADD COLUMN" in sql_content
