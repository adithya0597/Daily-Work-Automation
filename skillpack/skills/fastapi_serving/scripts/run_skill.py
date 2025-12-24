#!/usr/bin/env python3
"""Thin wrapper script for fastapi-serving skill."""

import argparse
import sys
from pathlib import Path

SKILLPACK_ROOT = Path(__file__).parent.parent.parent.parent / "skillpack"
if str(SKILLPACK_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLPACK_ROOT.parent))

from skillpack.skills.fastapi_serving import fastapi_serving_main


def main() -> int:
    parser = argparse.ArgumentParser(description="Wrap models in FastAPI services with validation and health endpoints")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("./out/fastapi_serving"))
    args = parser.parse_args()

    result = fastapi_serving_main(
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
