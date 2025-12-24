#!/usr/bin/env python3
"""Wrapper script for dag-authoring skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack dag-authoring --help
"""

import subprocess
import sys


def main() -> int:
    """Run the dag-authoring skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "dag-authoring"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
