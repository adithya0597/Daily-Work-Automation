#!/usr/bin/env python3
"""Thin wrapper script for daily-ops-summary skill."""

import argparse
import sys
from pathlib import Path

SKILLPACK_ROOT = Path(__file__).parent.parent.parent.parent / "skillpack"
if str(SKILLPACK_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLPACK_ROOT.parent))

from skillpack.skills.daily_ops_summary import daily_ops_summary_main


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate daily status report from pipeline and system health")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("./out/daily_ops_summary"))
    args = parser.parse_args()

    result = daily_ops_summary_main(
        input_path=args.input,
        output_dir=args.output_dir,
    )

    if result.get("success"):
        print(f"✅ Generated files in {args.output_dir}")
        return 0
    print(f"❌ Error: {result.get('error')}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
