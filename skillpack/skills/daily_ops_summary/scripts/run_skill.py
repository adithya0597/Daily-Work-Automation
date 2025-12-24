#!/usr/bin/env python3
"""Wrapper script for daily-ops-summary skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack daily-ops-summary --help
"""

import subprocess
import sys


def main() -> int:
    """Run the daily-ops-summary skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "daily-ops-summary"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
