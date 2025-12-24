#!/usr/bin/env python3
"""Wrapper script for iac-boilerplate skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack iac-boilerplate --help
"""

import subprocess
import sys


def main() -> int:
    """Run the iac-boilerplate skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "iac-boilerplate"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
