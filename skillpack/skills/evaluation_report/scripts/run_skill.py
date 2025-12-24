#!/usr/bin/env python3
"""Wrapper script for evaluation-report skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack evaluation-report --help
"""

import subprocess
import sys


def main() -> int:
    """Run the evaluation-report skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "evaluation-report"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
