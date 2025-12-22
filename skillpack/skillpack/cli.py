"""Skillpack CLI - Main entry point for all skills."""

import argparse
import sys

from skillpack import __version__
from skillpack.skills import (
    data_quality,
    dbt_generator,
    list_skills,
    pr_summary,
    profile_dataset,
    project_scaffolding,
    quality_gate,
    schema_diff,
    sql_refiner,
)
from skillpack.utils.logging import setup_logging


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with all skill subcommands."""
    parser = argparse.ArgumentParser(
        prog="skillpack",
        description="Production-grade engineering skills for daily work automation.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"skillpack {__version__}",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    subparsers = parser.add_subparsers(
        dest="skill",
        title="skills",
        description="Available skills",
        metavar="<skill>",
    )

    # Skill Discovery
    list_skills.register_parser(subparsers)

    # Phase 0: Foundation & Guardrails
    project_scaffolding.register_parser(subparsers)
    quality_gate.register_parser(subparsers)
    pr_summary.register_parser(subparsers)

    # Phase 1: Data Productivity
    profile_dataset.register_parser(subparsers)
    data_quality.register_parser(subparsers)
    sql_refiner.register_parser(subparsers)
    schema_diff.register_parser(subparsers)
    dbt_generator.register_parser(subparsers)

    return parser


def main() -> int:
    """Main entry point for the skillpack CLI."""
    parser = create_parser()
    args = parser.parse_args()

    # Set up logging
    import logging
    level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(level=level)

    if args.skill is None:
        parser.print_help()
        return 0

    # Execute the skill's handler
    if hasattr(args, "handler"):
        return args.handler(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
