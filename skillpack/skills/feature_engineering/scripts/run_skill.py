#!/usr/bin/env python3
"""Wrapper script for feature-engineering skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack feature-engineering --help
"""

import subprocess
import sys


def main() -> int:
    """Run the feature-engineering skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "feature-engineering"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
