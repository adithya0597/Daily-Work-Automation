#!/usr/bin/env python3
"""Wrapper script for containerization skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack containerization --help
"""

import subprocess
import sys


def main() -> int:
    """Run the containerization skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "containerization"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
