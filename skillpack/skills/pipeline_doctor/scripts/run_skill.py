#!/usr/bin/env python3
"""Wrapper script for pipeline-doctor skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack pipeline-doctor --help
"""

import subprocess
import sys


def main() -> int:
    """Run the pipeline-doctor skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    args = ["skillpack", "pipeline-doctor"] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
