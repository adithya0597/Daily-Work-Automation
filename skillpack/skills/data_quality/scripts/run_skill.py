#!/usr/bin/env python3
"""Wrapper script for data-quality skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack data-quality --help
"""

import subprocess
import sys


def main() -> int:
    """Run the data-quality skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "data-quality"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
