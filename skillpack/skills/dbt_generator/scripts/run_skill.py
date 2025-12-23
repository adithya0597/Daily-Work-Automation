#!/usr/bin/env python3
"""Thin wrapper script for dbt-generator skill.

This script provides an agent-editable interface to the dbt_generator skill.

Usage:
    python run_skill.py [--config CONFIG_PATH]
"""

import argparse
import sys
from pathlib import Path

# Add parent package to path for standalone execution
SKILLPACK_ROOT = Path(__file__).parent.parent.parent.parent / "skillpack"
if str(SKILLPACK_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLPACK_ROOT.parent))

from skillpack.skills.dbt_generator import generate_dbt


def main() -> int:
    """Main entry point for the skill wrapper."""
    parser = argparse.ArgumentParser(
        description="Generate dbt models, tests, and schema.yml"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to dbt configuration YAML file",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./out/dbt_generator"),
        help="Output directory",
    )

    args = parser.parse_args()

    # Call the core implementation
    result = generate_dbt(
        config_path=args.config,
        output_dir=args.output_dir,
    )

    if result.get("success"):
        print(f"✅ Generated dbt files in {args.output_dir}")
        return 0
    else:
        print(f"❌ Error: {result.get('error')}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
