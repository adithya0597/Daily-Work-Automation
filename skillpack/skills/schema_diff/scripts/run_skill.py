#!/usr/bin/env python3
"""Thin wrapper script for schema-diff skill.

This script provides an agent-editable interface to the schema_diff skill.

Usage:
    python run_skill.py --old OLD_SCHEMA --new NEW_SCHEMA [--table TABLE_NAME]
"""

import argparse
import sys
from pathlib import Path

# Add parent package to path for standalone execution
SKILLPACK_ROOT = Path(__file__).parent.parent.parent.parent / "skillpack"
if str(SKILLPACK_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLPACK_ROOT.parent))

from skillpack.skills.schema_diff import diff_schema


def main() -> int:
    """Main entry point for the skill wrapper."""
    parser = argparse.ArgumentParser(
        description="Compare database schemas and generate migration scripts"
    )
    parser.add_argument(
        "--old",
        type=Path,
        required=True,
        help="Path to old schema JSON",
    )
    parser.add_argument(
        "--new",
        type=Path,
        required=True,
        help="Path to new schema JSON",
    )
    parser.add_argument(
        "--table",
        default="table_name",
        help="Table name for SQL statements",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./out/schema_diff"),
        help="Output directory",
    )

    args = parser.parse_args()

    # Call the core implementation
    result = diff_schema(
        old_schema_path=args.old,
        new_schema_path=args.new,
        table_name=args.table,
        output_dir=args.output_dir,
    )

    if result.get("success"):
        print(f"✅ Generated migration files in {args.output_dir}")
        return 0
    else:
        print(f"❌ Error: {result.get('error')}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
