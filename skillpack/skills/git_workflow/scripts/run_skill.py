#!/usr/bin/env python3
"""Wrapper script for git-workflow skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack git-workflow --help
"""

import subprocess
import sys


def main() -> int:
    """Run the git-workflow skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "git-workflow"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
