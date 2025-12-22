"""Tests for sql_refiner skill."""

from pathlib import Path

import pytest

from skillpack.skills.sql_refiner import (
    extract_entities,
    generate_query_template,
    refine_sql,
)


def test_extract_entities_count() -> None:
    """Test entity extraction for count queries."""
    entities = extract_entities("How many users are there")
    assert "COUNT" in entities["aggregations"]


def test_extract_entities_average() -> None:
    """Test entity extraction for average queries."""
    entities = extract_entities("What is the average order value")
    assert "AVG" in entities["aggregations"]


def test_extract_entities_top() -> None:
    """Test entity extraction for top N queries."""
    entities = extract_entities("Get top 10 customers")
    assert entities["limit"] == 10
    assert entities["ordering"] == "DESC"


def test_generate_query_template_postgres() -> None:
    """Test query template generation for PostgreSQL."""
    query = generate_query_template("Count active users", "postgres")
    assert "SELECT" in query
    assert "COUNT" in query


def test_generate_query_template_bigquery() -> None:
    """Test query template generation for BigQuery."""
    query = generate_query_template("Top 5 orders", "bigquery")
    assert "SELECT" in query
    assert "LIMIT 5" in query


def test_refine_sql_creates_files(tmp_path: Path) -> None:
    """Test that refine_sql creates output files."""
    query_path, explain_path, notes_path = refine_sql(
        question="How many active users",
        dialect="postgres",
        base_dir=str(tmp_path / "out"),
    )

    assert query_path.exists()
    assert explain_path.exists()
    assert notes_path.exists()
    assert query_path.suffix == ".sql"
    assert explain_path.suffix == ".sql"
    assert notes_path.suffix == ".md"


def test_refine_sql_invalid_dialect(tmp_path: Path) -> None:
    """Test that invalid dialect raises error."""
    with pytest.raises(ValueError):
        refine_sql(
            question="test",
            dialect="invalid_dialect",
            base_dir=str(tmp_path / "out"),
        )
