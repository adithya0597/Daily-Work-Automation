"""Schema Diff Skill - Compare schemas and generate migrations."""

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from skillpack.utils.logging import get_logger
from skillpack.utils.output import get_output_dir

SKILL_NAME = "schema_diff"


@dataclass
class Column:
    """Represents a database column."""

    name: str
    type: str
    nullable: bool = True
    pk: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Column":
        """Create a Column from a dictionary."""
        return cls(
            name=data["name"],
            type=data["type"],
            nullable=data.get("nullable", True),
            pk=data.get("pk", False),
        )


@dataclass
class SchemaDiff:
    """Represents differences between two schemas."""

    added_columns: list[Column]
    removed_columns: list[Column]
    modified_columns: list[tuple[Column, Column]]  # (old, new)
    pk_changes: list[tuple[str, bool, bool]]  # (col_name, old_pk, new_pk)


def parse_schema(schema_path: str | Path) -> dict[str, Column]:
    """Parse a schema JSON file.

    Args:
        schema_path: Path to the schema JSON file.

    Returns:
        Dictionary mapping column names to Column objects.
    """
    path = Path(schema_path)
    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    columns = data.get("columns", [])
    return {col["name"]: Column.from_dict(col) for col in columns}


def diff_schemas(old_schema: dict[str, Column], new_schema: dict[str, Column]) -> SchemaDiff:
    """Compare two schemas and identify differences.

    Args:
        old_schema: The old schema.
        new_schema: The new schema.

    Returns:
        SchemaDiff with all differences.
    """
    old_names = set(old_schema.keys())
    new_names = set(new_schema.keys())

    added = [new_schema[name] for name in sorted(new_names - old_names)]
    removed = [old_schema[name] for name in sorted(old_names - new_names)]

    # Check for modifications in common columns
    modified = []
    pk_changes = []
    for name in sorted(old_names & new_names):
        old_col = old_schema[name]
        new_col = new_schema[name]

        if old_col.type != new_col.type or old_col.nullable != new_col.nullable:
            modified.append((old_col, new_col))

        if old_col.pk != new_col.pk:
            pk_changes.append((name, old_col.pk, new_col.pk))

    return SchemaDiff(
        added_columns=added,
        removed_columns=removed,
        modified_columns=modified,
        pk_changes=pk_changes,
    )


def generate_migration_sql(diff: SchemaDiff, table_name: str = "table_name") -> str:
    """Generate SQL migration statements.

    Args:
        diff: The schema diff.
        table_name: Name of the table.

    Returns:
        SQL migration script.
    """
    lines = [
        "-- Auto-generated migration script",
        f"-- Table: {table_name}",
        "",
        "-- ============================================",
        "-- MIGRATION: Forward",
        "-- ============================================",
        "",
    ]

    # Add columns
    for col in diff.added_columns:
        null_clause = "" if col.nullable else " NOT NULL"
        lines.append(f"ALTER TABLE {table_name} ADD COLUMN {col.name} {col.type}{null_clause};")

    if diff.added_columns:
        lines.append("")

    # Modify columns
    for old_col, new_col in diff.modified_columns:
        lines.append(f"-- Modify column: {old_col.name}")
        lines.append(f"-- Old: {old_col.type}, nullable={old_col.nullable}")
        lines.append(f"-- New: {new_col.type}, nullable={new_col.nullable}")

        if old_col.type != new_col.type:
            lines.append(
                f"ALTER TABLE {table_name} ALTER COLUMN {new_col.name} TYPE {new_col.type};"
            )

        if old_col.nullable and not new_col.nullable:
            lines.append(
                f"ALTER TABLE {table_name} ALTER COLUMN {new_col.name} SET NOT NULL;"
            )
        elif not old_col.nullable and new_col.nullable:
            lines.append(
                f"ALTER TABLE {table_name} ALTER COLUMN {new_col.name} DROP NOT NULL;"
            )
        lines.append("")

    # Remove columns (commented out for safety)
    if diff.removed_columns:
        lines.append("-- CAUTION: Column removals (uncomment to apply)")
        for col in diff.removed_columns:
            lines.append(f"-- ALTER TABLE {table_name} DROP COLUMN {col.name};")
        lines.append("")

    # PK changes
    if diff.pk_changes:
        lines.append("-- PRIMARY KEY changes")
        for col_name, old_pk, new_pk in diff.pk_changes:
            if old_pk and not new_pk:
                lines.append(f"-- Remove {col_name} from primary key")
            elif not old_pk and new_pk:
                lines.append(f"-- Add {col_name} to primary key")
        lines.append("")

    # Rollback section
    lines.extend([
        "-- ============================================",
        "-- ROLLBACK: Reverse migration",
        "-- ============================================",
        "",
    ])

    # Reverse add -> remove
    for col in diff.added_columns:
        lines.append(f"-- ALTER TABLE {table_name} DROP COLUMN {col.name};")

    # Reverse remove -> add
    for col in diff.removed_columns:
        null_clause = "" if col.nullable else " NOT NULL"
        lines.append(
            f"-- ALTER TABLE {table_name} ADD COLUMN {col.name} {col.type}{null_clause};"
        )

    return "\n".join(lines)


def generate_migration_notes(
    diff: SchemaDiff,
    old_path: str,
    new_path: str,
    table_name: str = "table_name",
) -> str:
    """Generate markdown notes about the migration.

    Args:
        diff: The schema diff.
        old_path: Path to old schema.
        new_path: Path to new schema.
        table_name: Name of the table.

    Returns:
        Markdown documentation.
    """
    lines = [
        "# Schema Migration Notes",
        "",
        "## Overview",
        "",
        f"- **Table:** `{table_name}`",
        f"- **Old Schema:** `{old_path}`",
        f"- **New Schema:** `{new_path}`",
        "",
        "## Changes Summary",
        "",
        f"- **Columns Added:** {len(diff.added_columns)}",
        f"- **Columns Removed:** {len(diff.removed_columns)}",
        f"- **Columns Modified:** {len(diff.modified_columns)}",
        f"- **PK Changes:** {len(diff.pk_changes)}",
        "",
    ]

    if diff.added_columns:
        lines.append("## Added Columns")
        lines.append("")
        for col in diff.added_columns:
            pk_badge = " (PK)" if col.pk else ""
            null_badge = " (nullable)" if col.nullable else " (NOT NULL)"
            lines.append(f"- `{col.name}`: {col.type}{null_badge}{pk_badge}")
        lines.append("")

    if diff.removed_columns:
        lines.append("## Removed Columns")
        lines.append("")
        lines.append("> ⚠️ **WARNING:** Removing columns may cause data loss!")
        lines.append("")
        for col in diff.removed_columns:
            lines.append(f"- `{col.name}`: {col.type}")
        lines.append("")

    if diff.modified_columns:
        lines.append("## Modified Columns")
        lines.append("")
        for old_col, new_col in diff.modified_columns:
            lines.append(f"### {old_col.name}")
            lines.append("")
            lines.append(f"| Property | Old | New |")
            lines.append(f"|----------|-----|-----|")
            lines.append(f"| Type | {old_col.type} | {new_col.type} |")
            lines.append(f"| Nullable | {old_col.nullable} | {new_col.nullable} |")
            lines.append("")
        lines.append("")

    lines.extend([
        "## Impact Assessment",
        "",
        "### Backfill Required",
        "",
    ])

    if diff.added_columns:
        non_null_added = [c for c in diff.added_columns if not c.nullable]
        if non_null_added:
            lines.append("The following new NOT NULL columns will need default values or backfill:")
            for col in non_null_added:
                lines.append(f"- `{col.name}`")
        else:
            lines.append("No backfill required for new columns (all nullable).")
    else:
        lines.append("No new columns added.")

    lines.extend([
        "",
        "### Rollback Plan",
        "",
        "1. Restore from backup if data loss occurred",
        "2. Run the rollback SQL statements in `migration.sql`",
        "3. Verify data integrity after rollback",
        "",
    ])

    return "\n".join(lines)


def diff_schema(
    old_path: str,
    new_path: str,
    table_name: str = "table_name",
    base_dir: str = "./out",
) -> tuple[Path, Path]:
    """Generate schema diff outputs.

    Args:
        old_path: Path to old schema JSON.
        new_path: Path to new schema JSON.
        table_name: Name of the table.
        base_dir: Base output directory.

    Returns:
        Tuple of (sql_path, notes_path).
    """
    logger = get_logger()

    logger.info(f"Comparing schemas: {old_path} -> {new_path}")

    old_schema = parse_schema(old_path)
    new_schema = parse_schema(new_path)

    diff = diff_schemas(old_schema, new_schema)

    sql_content = generate_migration_sql(diff, table_name)
    notes_content = generate_migration_notes(diff, old_path, new_path, table_name)

    output_dir = get_output_dir(SKILL_NAME, base_dir)

    sql_path = output_dir / "migration.sql"
    sql_path.write_text(sql_content, encoding="utf-8")

    notes_path = output_dir / "migration.md"
    notes_path.write_text(notes_content, encoding="utf-8")

    logger.info(f"Migration files generated in: {output_dir}")
    return sql_path, notes_path


def handler(args: argparse.Namespace) -> int:
    """Handle the schema-diff command."""
    try:
        sql_path, notes_path = diff_schema(
            old_path=args.old,
            new_path=args.new,
            table_name=args.table,
        )
        print(f"✅ Schema diff generated:")
        print(f"   SQL: {sql_path}")
        print(f"   Notes: {notes_path}")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def register_parser(subparsers: Any) -> None:
    """Register the schema-diff subcommand."""
    parser = subparsers.add_parser(
        "schema-diff",
        help="Compare schemas and generate migrations",
        description="Compares two schema JSON files and generates migration SQL with notes.",
    )
    parser.add_argument(
        "--old",
        required=True,
        help="Path to old schema JSON file",
    )
    parser.add_argument(
        "--new",
        required=True,
        help="Path to new schema JSON file",
    )
    parser.add_argument(
        "--table",
        default="table_name",
        help="Table name for the migration (default: table_name)",
    )
    parser.set_defaults(handler=handler)
