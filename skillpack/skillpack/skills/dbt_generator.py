"""dbt Generator Skill - Generate dbt models and tests."""

import argparse
from pathlib import Path
from typing import Any

import yaml

from skillpack.utils.config import load_config
from skillpack.utils.logging import get_logger
from skillpack.utils.output import get_output_dir

SKILL_NAME = "dbt_generator"


def generate_staging_model(source: dict[str, Any]) -> str:
    """Generate a staging model SQL file.

    Args:
        source: Source table configuration.

    Returns:
        SQL content for the staging model.
    """
    source_name = source.get("source_name", "raw")
    table_name = source.get("table_name")
    columns = source.get("columns", [])

    # Build column list with optional transformations
    col_lines = []
    for col in columns:
        col_name = col.get("name")
        alias = col.get("alias", col_name)
        transform = col.get("transform")

        if transform:
            col_lines.append(f"    {transform} AS {alias}")
        elif alias != col_name:
            col_lines.append(f"    {col_name} AS {alias}")
        else:
            col_lines.append(f"    {col_name}")

    columns_sql = ",\n".join(col_lines)

    return f'''{{{{ config(
    materialized='view',
    tags=['staging']
) }}}}

WITH source AS (
    SELECT * FROM {{{{ source('{source_name}', '{table_name}') }}}}
),

staged AS (
    SELECT
{columns_sql}
    FROM source
)

SELECT * FROM staged
'''


def generate_mart_model(model: dict[str, Any]) -> str:
    """Generate a mart model SQL file.

    Args:
        model: Model configuration.

    Returns:
        SQL content for the mart model.
    """
    name = model.get("name", "mart_model")
    description = model.get("description", "")
    refs = model.get("refs", [])
    columns = model.get("columns", [])
    filters = model.get("filters", [])
    aggregations = model.get("aggregations", [])
    group_by = model.get("group_by", [])

    # Build WITH clause for refs
    cte_lines = []
    for i, ref in enumerate(refs):
        ref_name = ref.get("name")
        alias = ref.get("alias", ref_name)
        cte_lines.append(f"{alias} AS (\n    SELECT * FROM {{{{ ref('{ref_name}') }}}}\n)")

    ctes = ",\n\n".join(cte_lines)

    # Build SELECT
    select_cols = []
    for col in columns:
        col_name = col.get("name")
        source = col.get("source", refs[0].get("alias") if refs else "source")
        select_cols.append(f"    {source}.{col_name}")

    for agg in aggregations:
        func = agg.get("function", "COUNT")
        col = agg.get("column", "*")
        alias = agg.get("alias", f"{func.lower()}_{col}")
        select_cols.append(f"    {func}({col}) AS {alias}")

    select_sql = ",\n".join(select_cols) if select_cols else "    *"

    # Build FROM
    main_table = refs[0].get("alias") if refs else "source"
    from_sql = f"FROM {main_table}"

    # Build WHERE
    where_sql = ""
    if filters:
        conditions = [f.get("condition") for f in filters if f.get("condition")]
        if conditions:
            where_sql = "\nWHERE " + "\n  AND ".join(conditions)

    # Build GROUP BY
    group_sql = ""
    if group_by:
        group_sql = "\nGROUP BY " + ", ".join(group_by)

    return f'''{{{{ config(
    materialized='table',
    tags=['mart']
) }}}}

-- {description}

WITH
{ctes}

SELECT
{select_sql}
{from_sql}{where_sql}{group_sql}
'''


def generate_schema_yml(config: dict[str, Any]) -> dict[str, Any]:
    """Generate schema.yml content.

    Args:
        config: Full configuration.

    Returns:
        Dictionary for schema.yml.
    """
    schema: dict[str, Any] = {
        "version": 2,
        "models": [],
    }

    # Add sources if defined
    sources = config.get("sources", [])
    if sources:
        schema["sources"] = []
        for source in sources:
            source_entry = {
                "name": source.get("source_name", "raw"),
                "tables": [
                    {
                        "name": source.get("table_name"),
                        "description": source.get("description", ""),
                    }
                ],
            }
            schema["sources"].append(source_entry)

    # Add staging models
    for source in sources:
        table_name = source.get("table_name")
        model_entry: dict[str, Any] = {
            "name": f"stg_{table_name}",
            "description": f"Staging model for {table_name}",
            "columns": [],
        }

        for col in source.get("columns", []):
            col_entry: dict[str, Any] = {
                "name": col.get("alias", col.get("name")),
            }
            if col.get("description"):
                col_entry["description"] = col.get("description")

            # Add tests
            tests = col.get("tests", [])
            if tests:
                col_entry["tests"] = tests

            model_entry["columns"].append(col_entry)

        schema["models"].append(model_entry)

    # Add mart models
    for model in config.get("models", []):
        model_entry = {
            "name": model.get("name"),
            "description": model.get("description", ""),
            "columns": [],
        }

        for col in model.get("columns", []):
            col_entry = {
                "name": col.get("name"),
            }
            if col.get("tests"):
                col_entry["tests"] = col.get("tests")
            model_entry["columns"].append(col_entry)

        schema["models"].append(model_entry)

    return schema


def generate_docs_block(config: dict[str, Any]) -> str:
    """Generate documentation blocks.

    Args:
        config: Full configuration.

    Returns:
        Markdown docs block content.
    """
    lines = ["{% docs __overview__ %}"]

    project_name = config.get("project_name", "dbt Project")
    lines.extend([
        f"# {project_name}",
        "",
        "## Overview",
        "",
        config.get("description", "Auto-generated dbt project."),
        "",
        "## Models",
        "",
    ])

    # Document staging models
    for source in config.get("sources", []):
        table_name = source.get("table_name")
        lines.append(f"### stg_{table_name}")
        lines.append("")
        lines.append(f"Staging model for `{table_name}` from the `{source.get('source_name')}` source.")
        lines.append("")

    # Document mart models
    for model in config.get("models", []):
        lines.append(f"### {model.get('name')}")
        lines.append("")
        lines.append(model.get("description", ""))
        lines.append("")

    lines.append("{% enddocs %}")

    return "\n".join(lines)


def get_example_config() -> dict[str, Any]:
    """Return an example configuration."""
    return {
        "project_name": "Example dbt Project",
        "description": "An example dbt project with users and orders.",
        "sources": [
            {
                "source_name": "raw",
                "table_name": "users",
                "description": "Raw users table",
                "columns": [
                    {"name": "id", "alias": "user_id", "tests": ["unique", "not_null"]},
                    {"name": "email", "tests": ["unique"]},
                    {"name": "created_at", "transform": "CAST(created_at AS TIMESTAMP)"},
                    {"name": "status"},
                ],
            },
            {
                "source_name": "raw",
                "table_name": "orders",
                "description": "Raw orders table",
                "columns": [
                    {"name": "id", "alias": "order_id", "tests": ["unique", "not_null"]},
                    {"name": "user_id", "tests": ["not_null"]},
                    {"name": "amount"},
                    {"name": "created_at"},
                ],
            },
        ],
        "models": [
            {
                "name": "mart_user_orders",
                "description": "User order summary mart",
                "refs": [
                    {"name": "stg_users", "alias": "users"},
                    {"name": "stg_orders", "alias": "orders"},
                ],
                "columns": [
                    {"name": "user_id", "source": "users"},
                    {"name": "email", "source": "users"},
                ],
                "aggregations": [
                    {"function": "COUNT", "column": "orders.order_id", "alias": "order_count"},
                    {"function": "SUM", "column": "orders.amount", "alias": "total_amount"},
                ],
                "group_by": ["users.user_id", "users.email"],
            },
        ],
    }


def generate_dbt(
    config_path: str | None = None,
    base_dir: str = "./out",
) -> Path:
    """Generate dbt models and schema from config.

    Args:
        config_path: Path to config file (YAML or JSON).
        base_dir: Base output directory.

    Returns:
        Path to the output directory.
    """
    logger = get_logger()

    if config_path:
        config = load_config(config_path)
    else:
        logger.info("No config provided, using example config")
        config = get_example_config()

    output_dir = get_output_dir(SKILL_NAME, base_dir)
    models_dir = output_dir / "models"
    staging_dir = models_dir / "staging"
    marts_dir = models_dir / "marts"

    staging_dir.mkdir(parents=True, exist_ok=True)
    marts_dir.mkdir(parents=True, exist_ok=True)

    # Generate staging models
    for source in config.get("sources", []):
        table_name = source.get("table_name")
        model_sql = generate_staging_model(source)
        model_path = staging_dir / f"stg_{table_name}.sql"
        model_path.write_text(model_sql, encoding="utf-8")
        logger.debug(f"Generated: {model_path}")

    # Generate mart models
    for model in config.get("models", []):
        model_name = model.get("name")
        model_sql = generate_mart_model(model)
        model_path = marts_dir / f"{model_name}.sql"
        model_path.write_text(model_sql, encoding="utf-8")
        logger.debug(f"Generated: {model_path}")

    # Generate schema.yml
    schema = generate_schema_yml(config)
    schema_path = models_dir / "schema.yml"
    schema_path.write_text(
        yaml.dump(schema, default_flow_style=False, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    logger.debug(f"Generated: {schema_path}")

    # Generate docs
    docs = generate_docs_block(config)
    docs_path = models_dir / "docs.md"
    docs_path.write_text(docs, encoding="utf-8")
    logger.debug(f"Generated: {docs_path}")

    logger.info(f"dbt files generated in: {output_dir}")
    return output_dir


def handler(args: argparse.Namespace) -> int:
    """Handle the dbt-generator command."""
    try:
        output_dir = generate_dbt(config_path=args.config)
        print(f"✅ dbt files generated in: {output_dir}")
        print(f"\nGenerated structure:")
        print(f"  {output_dir}/")
        print(f"  └── models/")
        print(f"      ├── staging/")
        print(f"      ├── marts/")
        print(f"      ├── schema.yml")
        print(f"      └── docs.md")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def register_parser(subparsers: Any) -> None:
    """Register the dbt-generator subcommand."""
    parser = subparsers.add_parser(
        "dbt-generator",
        help="Generate dbt models and tests",
        description="Generates dbt models, schema.yml, and documentation from a config file.",
    )
    parser.add_argument(
        "--config",
        required=False,
        help="Path to config file (YAML or JSON). If not provided, generates an example.",
    )
    parser.set_defaults(handler=handler)
