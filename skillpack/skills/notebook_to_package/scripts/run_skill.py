#!/usr/bin/env python3
"""Wrapper script for notebook-to-package skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack notebook-to-package --help
"""

import subprocess
import sys


def main() -> int:
    """Run the notebook-to-package skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "notebook-to-package"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
