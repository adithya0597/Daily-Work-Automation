#!/usr/bin/env python3
"""Wrapper script for experiment-tracking skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack experiment-tracking --help
"""

import subprocess
import sys


def main() -> int:
    """Run the experiment-tracking skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "experiment-tracking"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
