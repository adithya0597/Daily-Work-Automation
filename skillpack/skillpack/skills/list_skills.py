"""Skill Discovery CLI - List and inspect available skills."""

import argparse
import json
from typing import Any

from skillpack.utils.skill_loader import (
    export_skills_json,
    format_skill_for_llm,
    list_skills,
    load_skill,
)


def handler_list(args: argparse.Namespace) -> int:
    """Handle the list-skills list subcommand."""
    skills = list_skills()

    if args.format == "json":
        output = {"skills": skills}
        print(json.dumps(output, indent=2, ensure_ascii=False))
    elif args.format == "llm":
        # Export full skill definitions for LLM consumption
        print(export_skills_json())
    else:  # table format
        print(f"{'Skill Name':<25} {'Version':<10} {'Description'}")
        print("-" * 80)
        for skill in skills:
            name = skill.get("name", "unknown")
            version = skill.get("version", "0.0.0")
            desc = skill.get("description", "")[:45]
            print(f"{name:<25} {version:<10} {desc}")

    return 0


def handler_show(args: argparse.Namespace) -> int:
    """Handle the list-skills show subcommand."""
    try:
        if args.format == "llm":
            print(format_skill_for_llm(args.skill))
        elif args.format == "json":
            skill = load_skill(args.skill)
            print(json.dumps(skill, indent=2, ensure_ascii=False))
        else:  # yaml format
            skill = load_skill(args.skill)
            import yaml
            print(yaml.dump(skill, default_flow_style=False, allow_unicode=True, sort_keys=False))
        return 0
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1


def handler_guardrails(args: argparse.Namespace) -> int:
    """Handle the list-skills guardrails subcommand."""
    try:
        skill = load_skill(args.skill)
        guardrails = skill.get("guardrails", {})

        print(f"# Guardrails for: {args.skill}")
        print("")
        print("## ALLOWED")
        for item in guardrails.get("allowed", []):
            print(f"  ✓ {item}")
        print("")
        print("## FORBIDDEN (Never do these)")
        for item in guardrails.get("forbidden", []):
            print(f"  ✗ {item}")

        return 0
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1


def handler_command(args: argparse.Namespace) -> int:
    """Handle the list-skills command subcommand."""
    try:
        skill = load_skill(args.skill)
        cmd = skill.get("command", {})

        print(f"# Command for: {args.skill}")
        print("")
        print(f"Template: {cmd.get('template', 'N/A')}")
        print("")
        print("## Arguments")
        for arg_name, arg_spec in cmd.get("arguments", {}).items():
            required = "REQUIRED" if arg_spec.get("required", False) else "optional"
            cli_name = arg_spec.get("cli_name", f"--{arg_name}")
            print(f"  {cli_name} ({required})")
            print(f"    Type: {arg_spec.get('type', 'string')}")
            print(f"    Description: {arg_spec.get('description', 'No description')}")
            if arg_spec.get("default") is not None:
                print(f"    Default: {arg_spec.get('default')}")
            if arg_spec.get("validation"):
                print(f"    Validation: {arg_spec.get('validation')}")
            print("")

        return 0
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1


def handler(args: argparse.Namespace) -> int:
    """Handle the list-skills command."""
    if hasattr(args, "subhandler"):
        return args.subhandler(args)

    # Default: list skills
    args.format = getattr(args, "format", "table")
    return handler_list(args)


def register_parser(subparsers: Any) -> None:
    """Register the list-skills subcommand."""
    parser = subparsers.add_parser(
        "list-skills",
        help="List and inspect available skills",
        description="Discover skills, view their definitions, guardrails, and command specifications.",
    )
    parser.add_argument(
        "--format",
        choices=["table", "json", "llm"],
        default="table",
        help="Output format (default: table)",
    )

    skill_subparsers = parser.add_subparsers(
        dest="skill_command",
        title="commands",
        description="Skill inspection commands",
    )

    # list subcommand
    list_parser = skill_subparsers.add_parser(
        "list",
        help="List all available skills",
    )
    list_parser.add_argument(
        "--format",
        choices=["table", "json", "llm"],
        default="table",
        help="Output format",
    )
    list_parser.set_defaults(subhandler=handler_list)

    # show subcommand
    show_parser = skill_subparsers.add_parser(
        "show",
        help="Show full skill definition",
    )
    show_parser.add_argument(
        "skill",
        help="Skill name to show",
    )
    show_parser.add_argument(
        "--format",
        choices=["yaml", "json", "llm"],
        default="llm",
        help="Output format (default: llm)",
    )
    show_parser.set_defaults(subhandler=handler_show)

    # guardrails subcommand
    guardrails_parser = skill_subparsers.add_parser(
        "guardrails",
        help="Show skill guardrails (allowed/forbidden actions)",
    )
    guardrails_parser.add_argument(
        "skill",
        help="Skill name",
    )
    guardrails_parser.set_defaults(subhandler=handler_guardrails)

    # command subcommand
    command_parser = skill_subparsers.add_parser(
        "command",
        help="Show skill command specification",
    )
    command_parser.add_argument(
        "skill",
        help="Skill name",
    )
    command_parser.set_defaults(subhandler=handler_command)

    parser.set_defaults(handler=handler)
