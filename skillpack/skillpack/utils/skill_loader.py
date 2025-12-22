"""Skill loader utilities for reading and parsing skill definitions."""

import json
from pathlib import Path
from typing import Any

import yaml


def get_skills_directory() -> Path:
    """Get the path to the skills documentation directory.

    Returns:
        Path to the skills/ directory.
    """
    # Skills directory is at the repo root, sibling to skillpack package
    package_dir = Path(__file__).parent.parent
    repo_root = package_dir.parent
    return repo_root / "skills"


def load_skill(skill_name: str) -> dict[str, Any]:
    """Load a skill definition by name.

    Args:
        skill_name: Name of the skill (e.g., 'profile-dataset').

    Returns:
        Parsed skill definition as a dictionary.

    Raises:
        FileNotFoundError: If skill.yaml doesn't exist for the skill.
        ValueError: If skill.yaml is invalid.
    """
    # Convert CLI name to directory name (e.g., 'profile-dataset' -> 'profile_dataset')
    dir_name = skill_name.replace("-", "_")
    skills_dir = get_skills_directory()
    skill_file = skills_dir / dir_name / "skill.yaml"

    if not skill_file.exists():
        raise FileNotFoundError(f"Skill definition not found: {skill_file}")

    with open(skill_file, encoding="utf-8") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid skill.yaml for {skill_name}: {e}") from e


def list_skills() -> list[dict[str, Any]]:
    """List all available skills with their metadata.

    Returns:
        List of skill metadata dictionaries.
    """
    skills_dir = get_skills_directory()
    skills = []

    if not skills_dir.exists():
        return skills

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "skill.yaml"
        if skill_file.exists():
            try:
                with open(skill_file, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    skill_info = data.get("skill", {})
                    skill_info["directory"] = skill_dir.name
                    skill_info["path"] = str(skill_file)
                    skills.append(skill_info)
            except (yaml.YAMLError, OSError):
                # Skip invalid skill files
                continue

    return skills


def get_skill_command(skill_name: str) -> dict[str, Any]:
    """Get the command specification for a skill.

    Args:
        skill_name: Name of the skill.

    Returns:
        Command specification dictionary.
    """
    skill = load_skill(skill_name)
    return skill.get("command", {})


def get_skill_guardrails(skill_name: str) -> dict[str, Any]:
    """Get the guardrails for a skill.

    Args:
        skill_name: Name of the skill.

    Returns:
        Guardrails dictionary with 'allowed' and 'forbidden' lists.
    """
    skill = load_skill(skill_name)
    return skill.get("guardrails", {"allowed": [], "forbidden": []})


def get_skill_examples(skill_name: str) -> list[dict[str, Any]]:
    """Get the examples for a skill.

    Args:
        skill_name: Name of the skill.

    Returns:
        List of example dictionaries.
    """
    skill = load_skill(skill_name)
    return skill.get("examples", [])


def format_skill_for_llm(skill_name: str) -> str:
    """Format a skill definition for LLM consumption.

    Args:
        skill_name: Name of the skill.

    Returns:
        Formatted string representation of the skill.
    """
    skill = load_skill(skill_name)

    lines = []

    # Skill metadata
    info = skill.get("skill", {})
    lines.append(f"# Skill: {info.get('name', skill_name)}")
    lines.append(f"Description: {info.get('description', 'No description')}")
    lines.append(f"Tags: {', '.join(info.get('tags', []))}")
    lines.append("")

    # Command
    cmd = skill.get("command", {})
    lines.append("## Command")
    lines.append(f"Template: {cmd.get('template', 'N/A')}")
    lines.append("")
    lines.append("Arguments:")
    for arg_name, arg_spec in cmd.get("arguments", {}).items():
        required = "REQUIRED" if arg_spec.get("required", False) else "optional"
        lines.append(f"  - {arg_name} ({arg_spec.get('type', 'string')}, {required})")
        lines.append(f"    Description: {arg_spec.get('description', 'No description')}")
        if arg_spec.get("default") is not None:
            lines.append(f"    Default: {arg_spec.get('default')}")
    lines.append("")

    # Guardrails
    guardrails = skill.get("guardrails", {})
    lines.append("## Guardrails")
    lines.append("ALLOWED:")
    for item in guardrails.get("allowed", []):
        lines.append(f"  ✓ {item}")
    lines.append("FORBIDDEN:")
    for item in guardrails.get("forbidden", []):
        lines.append(f"  ✗ {item}")
    lines.append("")

    # Output
    output = skill.get("output", {})
    lines.append("## Output")
    if output.get("base_directory"):
        lines.append(f"Directory: {output.get('base_directory')}")
    for f in output.get("files", []):
        lines.append(f"  - {f.get('path')}: {f.get('description', '')}")
    lines.append("")

    # Examples
    examples = skill.get("examples", [])
    if examples:
        lines.append("## Examples")
        for ex in examples:
            lines.append(f"### {ex.get('name', 'Example')}")
            lines.append(f"Command: {ex.get('command', 'N/A')}")
            lines.append("")

    return "\n".join(lines)


def export_skills_json() -> str:
    """Export all skills as JSON for LLM consumption.

    Returns:
        JSON string with all skill definitions.
    """
    skills_data = []
    skills_dir = get_skills_directory()

    if not skills_dir.exists():
        return json.dumps({"skills": []}, indent=2)

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "skill.yaml"
        if skill_file.exists():
            try:
                with open(skill_file, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    skills_data.append(data)
            except (yaml.YAMLError, OSError):
                continue

    return json.dumps({"skills": skills_data}, indent=2, ensure_ascii=False)
