#!/usr/bin/env python3
"""Wrapper script for hyperparameter-search skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack hyperparameter-search --help
"""

import subprocess
import sys


def main() -> int:
    """Run the hyperparameter-search skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "hyperparameter-search"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
