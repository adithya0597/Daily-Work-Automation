"""Skillpack CLI - Main entry point for all skills."""

import argparse
import sys

from skillpack import __version__
from skillpack.skills import (
    backfill_planner,
    baseline_model_factory,
    dag_authoring,
    daily_ops_summary,
    data_quality,
    dbt_generator,
    evaluation_report,
    experiment_queue,
    experiment_tracking,
    feature_engineering,
    git_workflow,
    hyperparameter_search,
    list_skills,
    notebook_to_package,
    pipeline_doctor,
    pr_summary,
    profile_dataset,
    project_scaffolding,
    quality_gate,
    refactor_skill,
    schema_diff,
    sql_refiner,
    test_writer,
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

    # Productivity Layer
    git_workflow.register_parser(subparsers)
    notebook_to_package.register_parser(subparsers)
    test_writer.register_parser(subparsers)
    refactor_skill.register_parser(subparsers)

    # ETL/Orchestration Layer
    dag_authoring.register_parser(subparsers)
    backfill_planner.register_parser(subparsers)
    pipeline_doctor.register_parser(subparsers)
    daily_ops_summary.register_parser(subparsers)

    # ML Development Layer
    baseline_model_factory.register_parser(subparsers)
    feature_engineering.register_parser(subparsers)
    hyperparameter_search.register_parser(subparsers)
    experiment_tracking.register_parser(subparsers)
    evaluation_report.register_parser(subparsers)
    experiment_queue.register_parser(subparsers)

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
