#!/usr/bin/env python3
"""Wrapper script for cost-regression skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack cost-regression --help
"""

import subprocess
import sys


def main() -> int:
    """Run the cost-regression skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "cost-regression"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
