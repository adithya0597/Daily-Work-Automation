#!/usr/bin/env python3
"""Wrapper script for baseline-model-factory skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack baseline-model-factory --help
"""

import subprocess
import sys


def main() -> int:
    """Run the baseline-model-factory skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "baseline-model-factory"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
