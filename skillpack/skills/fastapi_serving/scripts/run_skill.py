#!/usr/bin/env python3
"""Wrapper script for fastapi-serving skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack fastapi-serving --help
"""

import subprocess
import sys


def main() -> int:
    """Run the fastapi-serving skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "fastapi-serving"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
