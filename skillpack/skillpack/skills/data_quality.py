"""Data Quality Skill - Generate Pandera validation schemas."""

import argparse
from pathlib import Path
from typing import Any

from skillpack.utils.config import load_config
from skillpack.utils.logging import get_logger
from skillpack.utils.output import get_output_dir, write_text

SKILL_NAME = "data_quality"

# Type mapping from config types to Pandera types
TYPE_MAPPING = {
    "string": "str",
    "str": "str",
    "integer": "int",
    "int": "int",
    "float": "float",
    "number": "float",
    "boolean": "bool",
    "bool": "bool",
    "datetime": "datetime64[ns]",
    "date": "datetime64[ns]",
}


def generate_pandera_schema(config: dict[str, Any]) -> str:
    """Generate Pandera schema code from config.

    Args:
        config: Configuration with columns and constraints.

    Returns:
        Python code string for the Pandera schema.
    """
    schema_name = config.get("name", "DataSchema")
    columns = config.get("columns", [])

    lines = [
        '"""Auto-generated Pandera schema for data validation."""',
        "",
        "import pandera as pa",
        "from pandera import Column, Check, DataFrameSchema",
        "",
        "",
        f"# Schema: {schema_name}",
        f"{schema_name} = DataFrameSchema(",
        "    columns={",
    ]

    for col in columns:
        col_name = col.get("name")
        col_type = col.get("type", "string")
        nullable = col.get("nullable", True)
        unique = col.get("unique", False)
        checks = col.get("checks", [])

        pa_type = TYPE_MAPPING.get(col_type.lower(), "str")

        # Build checks list
        check_strs = []
        for check in checks:
            check_type = check.get("type")
            if check_type == "min":
                check_strs.append(f"Check.ge({check.get('value')})")
            elif check_type == "max":
                check_strs.append(f"Check.le({check.get('value')})")
            elif check_type == "regex":
                pattern = check.get("pattern", ".*")
                check_strs.append(f'Check.str_matches(r"{pattern}")')
            elif check_type == "isin":
                values = check.get("values", [])
                check_strs.append(f"Check.isin({values})")
            elif check_type == "between":
                min_val = check.get("min")
                max_val = check.get("max")
                check_strs.append(f"Check.in_range({min_val}, {max_val})")

        # Build column definition
        checks_arg = f", checks=[{', '.join(check_strs)}]" if check_strs else ""
        unique_arg = ", unique=True" if unique else ""

        lines.append(
            f'        "{col_name}": Column(pa.{pa_type.capitalize() if pa_type in ("str", "int", "float", "bool") else pa_type}, '
            f"nullable={nullable}{unique_arg}{checks_arg}),"
        )

    lines.extend([
        "    },",
        f'    name="{schema_name}",',
        "    strict=False,",
        "    coerce=True,",
        ")",
        "",
        "",
        "def validate(df):",
        '    """Validate a DataFrame against the schema."""',
        f"    return {schema_name}.validate(df)",
        "",
    ])

    return "\n".join(lines)


def generate_runner(config: dict[str, Any]) -> str:
    """Generate a validation runner script.

    Args:
        config: Configuration with columns and constraints.

    Returns:
        Python code string for the runner.
    """
    schema_name = config.get("name", "DataSchema")

    return f'''"""Runner script for data validation."""

import sys
import pandas as pd
from schema import {schema_name}, validate


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_validation.py <csv_file>")
        sys.exit(1)

    csv_path = sys.argv[1]
    print(f"Loading: {{csv_path}}")

    df = pd.read_csv(csv_path)
    print(f"Loaded {{len(df)}} rows")

    try:
        validated_df = validate(df)
        print(f"✅ Validation passed! {{len(validated_df)}} rows valid.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Validation failed: {{e}}")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''


def generate_example_config() -> dict[str, Any]:
    """Generate an example configuration."""
    return {
        "name": "UserSchema",
        "columns": [
            {
                "name": "id",
                "type": "integer",
                "nullable": False,
                "unique": True,
                "checks": [{"type": "min", "value": 1}],
            },
            {
                "name": "email",
                "type": "string",
                "nullable": False,
                "checks": [{"type": "regex", "pattern": r"^[\w\.-]+@[\w\.-]+\.\w+$"}],
            },
            {
                "name": "age",
                "type": "integer",
                "nullable": True,
                "checks": [{"type": "between", "min": 0, "max": 150}],
            },
            {
                "name": "status",
                "type": "string",
                "nullable": False,
                "checks": [{"type": "isin", "values": ["active", "inactive", "pending"]}],
            },
        ],
    }


def generate_data_quality(
    config_path: str | None = None,
    base_dir: str = "./out",
) -> tuple[Path, Path]:
    """Generate Pandera schema and runner from config.

    Args:
        config_path: Path to config file (YAML or JSON).
        base_dir: Base output directory.

    Returns:
        Tuple of (schema_path, runner_path).
    """
    logger = get_logger()

    if config_path:
        config = load_config(config_path)
    else:
        logger.info("No config provided, using example config")
        config = generate_example_config()

    output_dir = get_output_dir(SKILL_NAME, base_dir)

    # Generate schema
    schema_code = generate_pandera_schema(config)
    schema_path = output_dir / "schema.py"
    schema_path.write_text(schema_code, encoding="utf-8")
    logger.info(f"Schema generated: {schema_path}")

    # Generate runner
    runner_code = generate_runner(config)
    runner_path = output_dir / "run_validation.py"
    runner_path.write_text(runner_code, encoding="utf-8")
    logger.info(f"Runner generated: {runner_path}")

    return schema_path, runner_path


def handler(args: argparse.Namespace) -> int:
    """Handle the data-quality command."""
    try:
        schema_path, runner_path = generate_data_quality(
            config_path=args.config,
        )
        print(f"✅ Data quality files generated:")
        print(f"   Schema: {schema_path}")
        print(f"   Runner: {runner_path}")
        print(f"\nUsage: python {runner_path} <csv_file>")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def register_parser(subparsers: Any) -> None:
    """Register the data-quality subcommand."""
    parser = subparsers.add_parser(
        "data-quality",
        help="Generate Pandera validation schema",
        description="Generates a Pandera schema and validation runner from a config file.",
    )
    parser.add_argument(
        "--config",
        required=False,
        help="Path to config file (YAML or JSON). If not provided, generates an example.",
    )
    parser.set_defaults(handler=handler)
