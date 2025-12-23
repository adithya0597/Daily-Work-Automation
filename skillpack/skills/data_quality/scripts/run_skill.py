#!/usr/bin/env python3
"""Thin wrapper script for data-quality skill.

This script provides an agent-editable interface to the data_quality skill.
It imports from the main skillpack package, allowing agents to:
1. Understand the interface by reading this file
2. Modify behavior without touching the core package

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

from skillpack.skills.data_quality import generate_data_quality


def main() -> int:
    """Main entry point for the skill wrapper."""
    parser = argparse.ArgumentParser(
        description="Generate Pandera validation schemas for DataFrames"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to schema configuration YAML file",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./out/data_quality"),
        help="Output directory (default: ./out/data_quality)",
    )

    args = parser.parse_args()

    # Call the core implementation
    result = generate_data_quality(
        config_path=args.config,
        output_dir=args.output_dir,
    )

    if result.get("success"):
        print(f"✅ Generated files in {args.output_dir}")
        return 0
    else:
        print(f"❌ Error: {result.get('error')}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
