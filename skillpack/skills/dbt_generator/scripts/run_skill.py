#!/usr/bin/env python3
"""Wrapper script for dbt-generator skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack dbt-generator --help
"""

import subprocess
import sys


def main() -> int:
    """Run the dbt-generator skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "dbt-generator"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
