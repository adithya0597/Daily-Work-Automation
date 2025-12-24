#!/usr/bin/env python3
"""Wrapper script for experiment-queue skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack experiment-queue --help
"""

import subprocess
import sys


def main() -> int:
    """Run the experiment-queue skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "experiment-queue"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
