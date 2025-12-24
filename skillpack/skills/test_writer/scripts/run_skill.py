#!/usr/bin/env python3
"""Wrapper script for test-writer skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack test-writer --help
"""

import subprocess
import sys


def main() -> int:
    """Run the test-writer skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "test-writer"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
