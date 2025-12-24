#!/usr/bin/env python3
"""Wrapper script for refactor-skill skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack refactor-skill --help
"""

import subprocess
import sys


def main() -> int:
    """Run the refactor-skill skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "refactor-skill"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
