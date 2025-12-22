"""Safe output file writing utilities."""

import json
from pathlib import Path
from typing import Any

import yaml


def get_output_dir(skill_name: str, base_dir: str = "./out") -> Path:
    """Get the output directory for a skill, creating it if needed.

    Args:
        skill_name: Name of the skill (used as subdirectory name).
        base_dir: Base output directory (default: ./out).

    Returns:
        Path to the skill's output directory.
    """
    output_dir = Path(base_dir) / skill_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def write_text(
    content: str,
    filename: str,
    skill_name: str,
    subdir: str | None = None,
    base_dir: str = "./out",
) -> Path:
    """Write text content to a file in the skill's output directory.

    Args:
        content: Text content to write.
        filename: Name of the output file.
        skill_name: Name of the skill.
        subdir: Optional subdirectory within the skill's output directory.
        base_dir: Base output directory.

    Returns:
        Path to the written file.
    """
    output_dir = get_output_dir(skill_name, base_dir)
    if subdir:
        output_dir = output_dir / subdir
        output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename
    output_path.write_text(content, encoding="utf-8")
    return output_path


def write_json(
    data: dict[str, Any] | list[Any],
    filename: str,
    skill_name: str,
    subdir: str | None = None,
    base_dir: str = "./out",
    indent: int = 2,
) -> Path:
    """Write JSON data to a file in the skill's output directory.

    Args:
        data: Data to serialize as JSON.
        filename: Name of the output file.
        skill_name: Name of the skill.
        subdir: Optional subdirectory within the skill's output directory.
        base_dir: Base output directory.
        indent: JSON indentation level.

    Returns:
        Path to the written file.
    """
    content = json.dumps(data, indent=indent, ensure_ascii=False, sort_keys=True)
    return write_text(content, filename, skill_name, subdir, base_dir)


def write_yaml(
    data: dict[str, Any] | list[Any],
    filename: str,
    skill_name: str,
    subdir: str | None = None,
    base_dir: str = "./out",
) -> Path:
    """Write YAML data to a file in the skill's output directory.

    Args:
        data: Data to serialize as YAML.
        filename: Name of the output file.
        skill_name: Name of the skill.
        subdir: Optional subdirectory within the skill's output directory.
        base_dir: Base output directory.

    Returns:
        Path to the written file.
    """
    content = yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=True)
    return write_text(content, filename, skill_name, subdir, base_dir)
