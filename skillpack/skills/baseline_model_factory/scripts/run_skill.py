#!/usr/bin/env python3
"""Thin wrapper script for baseline-model-factory skill."""

import argparse
import sys
from pathlib import Path

SKILLPACK_ROOT = Path(__file__).parent.parent.parent.parent / "skillpack"
if str(SKILLPACK_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLPACK_ROOT.parent))

from skillpack.skills.baseline_model_factory import baseline_model_factory_main


def main() -> int:
    parser = argparse.ArgumentParser(description="Build scikit-learn baselines with proper pipelines and config")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("./out/baseline_model_factory"))
    args = parser.parse_args()

    result = baseline_model_factory_main(
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
