#!/usr/bin/env python3
"""Wrapper script for schema-diff skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack schema-diff --help
"""

import subprocess
import sys


def main() -> int:
    """Run the schema-diff skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "schema-diff"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
