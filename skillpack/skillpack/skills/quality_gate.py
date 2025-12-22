"""Quality Gate Skill - Run format + lint + type-check + tests."""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

from skillpack.utils.logging import get_logger

SKILL_NAME = "quality_gate"


def run_command(cmd: list[str], check: bool = False) -> tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr.

    Args:
        cmd: Command and arguments to run.
        check: If True, only check without fixing.

    Returns:
        Tuple of (exit_code, stdout, stderr).
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        return 1, "", f"Command not found: {cmd[0]}"


def run_quality_gate(check_only: bool = False) -> int:
    """Run the full quality gate.

    Args:
        check_only: If True, only check without modifying files.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    logger = get_logger()
    exit_code = 0

    steps = [
        ("Format", ["ruff", "format"] + (["--check"] if check_only else []) + ["."]),
        ("Lint", ["ruff", "check"] + ([] if check_only else ["--fix"]) + ["."]),
        ("Type Check", ["mypy", "skillpack/"]),
        ("Tests", ["pytest", "tests/", "-v"]),
    ]

    for name, cmd in steps:
        logger.info(f"Running: {name}")
        code, stdout, stderr = run_command(cmd)

        if stdout:
            print(stdout)
        if stderr:
            print(stderr, file=sys.stderr)

        if code != 0:
            logger.error(f"❌ {name} failed with exit code {code}")
            exit_code = code
            # Continue running other checks even if one fails
        else:
            logger.info(f"✅ {name} passed")

    return exit_code


def handler(args: argparse.Namespace) -> int:
    """Handle the quality-gate command."""
    return run_quality_gate(check_only=args.check)


def register_parser(subparsers: Any) -> None:
    """Register the quality-gate subcommand."""
    parser = subparsers.add_parser(
        "quality-gate",
        help="Run format + lint + type-check + tests",
        description="Runs the full quality gate: formatting, linting, type checking, and tests.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check only, don't modify files",
    )
    parser.set_defaults(handler=handler)
