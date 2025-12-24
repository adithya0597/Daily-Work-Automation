#!/usr/bin/env python3
"""Wrapper script for skill.

This delegates to the main skillpack CLI. For direct usage:
    skillpack <skill-name> --help
"""

import subprocess
import sys


def main() -> int:
    """Run the skill via the CLI."""
    # Pass all arguments through to the skillpack CLI
    skill_name = __file__.split("/")[-3].replace("_", "-")
    args = ["skillpack", skill_name] + sys.argv[1:]
    return subprocess.call(args)


if __name__ == "__main__":
    sys.exit(main())
