"""SQL Query Refiner Skill - Generate SQL queries from natural language questions."""

import argparse
import re
from pathlib import Path
from typing import Any

from skillpack.utils.logging import get_logger
from skillpack.utils.output import get_output_dir, write_text

SKILL_NAME = "sql_refiner"

# Dialect-specific syntax differences
DIALECT_CONFIG = {
    "postgres": {
        "string_agg": "STRING_AGG({col}, ', ')",
        "date_trunc": "DATE_TRUNC('{unit}', {col})",
        "current_timestamp": "CURRENT_TIMESTAMP",
        "limit": "LIMIT {n}",
        "ilike": "ILIKE",
        "concat": "{a} || {b}",
        "bool_type": "BOOLEAN",
        "json_extract": "{col}->'{key}'",
    },
    "bigquery": {
        "string_agg": "STRING_AGG({col}, ', ')",
        "date_trunc": "DATE_TRUNC({col}, {unit})",
        "current_timestamp": "CURRENT_TIMESTAMP()",
        "limit": "LIMIT {n}",
        "ilike": "LIKE",  # BigQuery doesn't have ILIKE
        "concat": "CONCAT({a}, {b})",
        "bool_type": "BOOL",
        "json_extract": "JSON_EXTRACT({col}, '$.{key}')",
    },
    "snowflake": {
        "string_agg": "LISTAGG({col}, ', ')",
        "date_trunc": "DATE_TRUNC('{unit}', {col})",
        "current_timestamp": "CURRENT_TIMESTAMP()",
        "limit": "LIMIT {n}",
        "ilike": "ILIKE",
        "concat": "{a} || {b}",
        "bool_type": "BOOLEAN",
        "json_extract": "{col}:{key}",
    },
}


def extract_entities(question: str) -> dict[str, Any]:
    """Extract potential entities from a natural language question.

    Args:
        question: The natural language question.

    Returns:
        Dictionary with extracted entities.
    """
    entities: dict[str, Any] = {
        "tables": [],
        "columns": [],
        "conditions": [],
        "aggregations": [],
        "ordering": None,
        "limit": None,
    }

    question_lower = question.lower()

    # Common aggregation patterns
    if any(word in question_lower for word in ["count", "how many"]):
        entities["aggregations"].append("COUNT")
    if any(word in question_lower for word in ["sum", "total"]):
        entities["aggregations"].append("SUM")
    if any(word in question_lower for word in ["average", "avg", "mean"]):
        entities["aggregations"].append("AVG")
    if any(word in question_lower for word in ["maximum", "max", "highest", "largest"]):
        entities["aggregations"].append("MAX")
    if any(word in question_lower for word in ["minimum", "min", "lowest", "smallest"]):
        entities["aggregations"].append("MIN")

    # Common condition patterns
    if "active" in question_lower:
        entities["conditions"].append("status = 'active'")
    if "last" in question_lower:
        # Try to extract time period
        time_match = re.search(r"last (\d+) (day|week|month|year)s?", question_lower)
        if time_match:
            num, unit = time_match.groups()
            entities["conditions"].append(f"created_at >= NOW() - INTERVAL '{num} {unit}s'")

    # Ordering
    if any(word in question_lower for word in ["top", "highest", "largest"]):
        entities["ordering"] = "DESC"
    if any(word in question_lower for word in ["bottom", "lowest", "smallest"]):
        entities["ordering"] = "ASC"

    # Limit
    limit_match = re.search(r"(top|first|last) (\d+)", question_lower)
    if limit_match:
        entities["limit"] = int(limit_match.group(2))
    elif "top" in question_lower or "first" in question_lower:
        entities["limit"] = 10  # Default limit

    return entities


def generate_query_template(question: str, dialect: str) -> str:
    """Generate a SQL query template from a question.

    Args:
        question: The natural language question.
        dialect: SQL dialect (postgres, bigquery, snowflake).

    Returns:
        SQL query string.
    """
    entities = extract_entities(question)
    config = DIALECT_CONFIG.get(dialect, DIALECT_CONFIG["postgres"])

    # Build basic query structure
    lines = []

    # Determine SELECT clause
    if entities["aggregations"]:
        agg = entities["aggregations"][0]
        lines.append(f"SELECT {agg}(*) AS result")
    else:
        lines.append("SELECT *")

    # Add FROM clause (placeholder)
    lines.append("FROM <table_name>")

    # Add WHERE clause if conditions exist
    if entities["conditions"]:
        lines.append("WHERE " + " AND ".join(entities["conditions"]))
    else:
        lines.append("WHERE 1=1  -- Add your conditions here")

    # Add GROUP BY if aggregating
    if entities["aggregations"] and "group" in question.lower():
        lines.append("GROUP BY <group_column>")

    # Add ORDER BY
    if entities["ordering"]:
        lines.append(f"ORDER BY result {entities['ordering']}")

    # Add LIMIT
    if entities["limit"]:
        lines.append(config["limit"].format(n=entities["limit"]))

    return "\n".join(lines) + ";"


def generate_explain_query(query: str, dialect: str) -> str:
    """Generate an EXPLAIN query for the given query.

    Args:
        query: The SQL query.
        dialect: SQL dialect.

    Returns:
        EXPLAIN query string.
    """
    if dialect == "postgres":
        return f"EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)\n{query}"
    elif dialect == "bigquery":
        return f"-- BigQuery: Use Query Plan in the Console\n{query}"
    elif dialect == "snowflake":
        return f"EXPLAIN\n{query}"
    return f"EXPLAIN\n{query}"


def generate_notes(question: str, query: str, dialect: str) -> str:
    """Generate notes about the query.

    Args:
        question: The original question.
        query: The generated query.
        dialect: SQL dialect.

    Returns:
        Markdown notes.
    """
    entities = extract_entities(question)

    lines = [
        "# Query Notes",
        "",
        "## Original Question",
        "",
        f"> {question}",
        "",
        "## Dialect",
        "",
        f"**{dialect.upper()}**",
        "",
        "## Query Analysis",
        "",
    ]

    if entities["aggregations"]:
        lines.append(f"- **Aggregations detected:** {', '.join(entities['aggregations'])}")
    if entities["conditions"]:
        lines.append(f"- **Conditions detected:** {len(entities['conditions'])}")
    if entities["limit"]:
        lines.append(f"- **Limit:** {entities['limit']}")
    if entities["ordering"]:
        lines.append(f"- **Ordering:** {entities['ordering']}")

    lines.extend([
        "",
        "## Placeholders to Replace",
        "",
        "- `<table_name>`: Replace with actual table name",
        "- `<group_column>`: Replace with column to group by (if applicable)",
        "",
        "## Performance Tips",
        "",
        "1. Ensure indexed columns are used in WHERE clause",
        "2. Avoid SELECT * in production queries",
        "3. Use appropriate data types for comparisons",
        "4. Consider partitioning for large tables",
        "",
        "## Generated Query",
        "",
        "```sql",
        query,
        "```",
        "",
    ])

    return "\n".join(lines)


def refine_sql(
    question: str,
    dialect: str = "postgres",
    base_dir: str = "./out",
) -> tuple[Path, Path, Path]:
    """Generate SQL query files from a question.

    Args:
        question: Natural language question.
        dialect: SQL dialect (postgres, bigquery, snowflake).
        base_dir: Base output directory.

    Returns:
        Tuple of (query_path, explain_path, notes_path).
    """
    logger = get_logger()

    if dialect not in DIALECT_CONFIG:
        raise ValueError(f"Unsupported dialect: {dialect}. Use: {list(DIALECT_CONFIG.keys())}")

    logger.info(f"Generating {dialect} SQL for: {question}")

    # Generate query
    query = generate_query_template(question, dialect)
    explain = generate_explain_query(query, dialect)
    notes = generate_notes(question, query, dialect)

    output_dir = get_output_dir(SKILL_NAME, base_dir)

    # Write files
    query_path = output_dir / "query.sql"
    query_path.write_text(query, encoding="utf-8")

    explain_path = output_dir / "explain.sql"
    explain_path.write_text(explain, encoding="utf-8")

    notes_path = output_dir / "query_notes.md"
    notes_path.write_text(notes, encoding="utf-8")

    logger.info(f"Files generated in: {output_dir}")
    return query_path, explain_path, notes_path


def handler(args: argparse.Namespace) -> int:
    """Handle the sql-refiner command."""
    try:
        query_path, explain_path, notes_path = refine_sql(
            question=args.question,
            dialect=args.dialect,
        )
        print(f"✅ SQL files generated:")
        print(f"   Query: {query_path}")
        print(f"   Explain: {explain_path}")
        print(f"   Notes: {notes_path}")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def register_parser(subparsers: Any) -> None:
    """Register the sql-refiner subcommand."""
    parser = subparsers.add_parser(
        "sql-refiner",
        help="Generate SQL from natural language",
        description="Generates SQL query, explain plan, and notes from a natural language question.",
    )
    parser.add_argument(
        "--question",
        required=True,
        help="Natural language question to convert to SQL",
    )
    parser.add_argument(
        "--dialect",
        choices=["postgres", "bigquery", "snowflake"],
        default="postgres",
        help="SQL dialect (default: postgres)",
    )
    parser.set_defaults(handler=handler)
