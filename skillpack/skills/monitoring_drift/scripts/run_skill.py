#!/usr/bin/env python3
"""Wrapper script for monitoring-drift skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack monitoring-drift --help
"""

import subprocess
import sys


def main() -> int:
    """Run the monitoring-drift skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "monitoring-drift"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
