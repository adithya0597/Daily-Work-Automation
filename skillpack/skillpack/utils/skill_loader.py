"""Skill loader utilities with progressive disclosure support.

This module implements a 3-tier progressive disclosure system:
- Tier 1: Metadata only (metadata.yaml) - always loaded, ~50 tokens
- Tier 2: Skill procedure (skill.md) - loaded on selection, ~500 tokens  
- Tier 3: Extended docs + scripts - loaded on execution

Usage:
    from skillpack.utils.skill_loader import (
        list_skills,           # Tier 1: Get all skill metadata
        load_skill,            # Tier 2: Get metadata + skill.md
        load_skill_full,       # Tier 3: Get everything
    )
"""

import json
from pathlib import Path
from typing import Any

import yaml


def get_skills_directory() -> Path:
    """Get the path to the skills documentation directory.

    Returns:
        Path to the skills/ directory.
    """
    package_dir = Path(__file__).parent.parent
    repo_root = package_dir.parent
    return repo_root / "skills"


def _normalize_skill_name(skill_name: str) -> str:
    """Convert CLI name to directory name.
    
    Args:
        skill_name: Skill name (e.g., 'profile-dataset')
        
    Returns:
        Directory name (e.g., 'profile_dataset')
    """
    return skill_name.replace("-", "_")


# =============================================================================
# TIER 1: Metadata Only (Always Loaded)
# =============================================================================

def list_skills() -> list[dict[str, Any]]:
    """List all available skills with compact metadata (Tier 1).

    Returns only the essential metadata for each skill, designed
    to be always in context for an LLM (~50 tokens per skill).

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

        # Try new format first (metadata.yaml)
        metadata_file = skill_dir / "metadata.yaml"
        if metadata_file.exists():
            try:
                with open(metadata_file, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    data["_directory"] = skill_dir.name
                    data["_path"] = str(metadata_file)
                    skills.append(data)
            except (yaml.YAMLError, OSError):
                continue
        else:
            # Fall back to old format (skill.yaml)
            skill_file = skill_dir / "skill.yaml"
            if skill_file.exists():
                try:
                    with open(skill_file, encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        skill_info = data.get("skill", {})
                        skill_info["_directory"] = skill_dir.name
                        skill_info["_path"] = str(skill_file)
                        skills.append(skill_info)
                except (yaml.YAMLError, OSError):
                    continue

    return skills


def get_skill_metadata(skill_name: str) -> dict[str, Any]:
    """Get metadata for a specific skill (Tier 1).

    Args:
        skill_name: Name of the skill.

    Returns:
        Metadata dictionary.

    Raises:
        FileNotFoundError: If skill doesn't exist.
    """
    dir_name = _normalize_skill_name(skill_name)
    skills_dir = get_skills_directory()
    
    metadata_file = skills_dir / dir_name / "metadata.yaml"
    if metadata_file.exists():
        with open(metadata_file, encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    # Fall back to old format
    skill_file = skills_dir / dir_name / "skill.yaml"
    if skill_file.exists():
        with open(skill_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data.get("skill", data)
    
    raise FileNotFoundError(f"Skill not found: {skill_name}")


# =============================================================================
# TIER 2: Skill Procedure (On Selection)
# =============================================================================

def load_skill(skill_name: str) -> dict[str, Any]:
    """Load skill metadata and procedure (Tier 2).

    Includes metadata.yaml contents plus skill.md content.
    This is what an LLM should load when selecting a skill.

    Args:
        skill_name: Name of the skill.

    Returns:
        Dictionary with metadata and skill_md content.

    Raises:
        FileNotFoundError: If skill doesn't exist.
    """
    dir_name = _normalize_skill_name(skill_name)
    skills_dir = get_skills_directory()
    skill_dir = skills_dir / dir_name

    if not skill_dir.exists():
        raise FileNotFoundError(f"Skill directory not found: {skill_dir}")

    result = get_skill_metadata(skill_name)
    result["_tier"] = 2

    # Load skill.md if exists
    skill_md = skill_dir / "skill.md"
    if skill_md.exists():
        result["skill_md"] = skill_md.read_text(encoding="utf-8")

    # List available docs and scripts
    docs_dir = skill_dir / "docs"
    scripts_dir = skill_dir / "scripts"
    
    result["available_docs"] = []
    if docs_dir.exists():
        result["available_docs"] = [f.name for f in docs_dir.glob("*.md")]

    result["available_scripts"] = []
    if scripts_dir.exists():
        result["available_scripts"] = [f.name for f in scripts_dir.glob("*.py")]

    return result


# =============================================================================
# TIER 3: Full Content (On Execution)
# =============================================================================

def load_skill_full(skill_name: str) -> dict[str, Any]:
    """Load complete skill content including docs and scripts (Tier 3).

    Args:
        skill_name: Name of the skill.

    Returns:
        Complete skill dictionary with all content.

    Raises:
        FileNotFoundError: If skill doesn't exist.
    """
    result = load_skill(skill_name)
    result["_tier"] = 3

    dir_name = _normalize_skill_name(skill_name)
    skills_dir = get_skills_directory()
    skill_dir = skills_dir / dir_name

    # Load all docs
    result["docs"] = {}
    docs_dir = skill_dir / "docs"
    if docs_dir.exists():
        for doc_file in docs_dir.glob("*.md"):
            result["docs"][doc_file.name] = doc_file.read_text(encoding="utf-8")

    # Load all scripts (just the code, for LLM understanding)
    result["scripts"] = {}
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        for script_file in scripts_dir.glob("*.py"):
            result["scripts"][script_file.name] = script_file.read_text(encoding="utf-8")

    # Load examples
    result["examples_content"] = {}
    examples_dir = skill_dir / "examples"
    if examples_dir.exists():
        for example_file in examples_dir.iterdir():
            if example_file.is_file():
                try:
                    result["examples_content"][example_file.name] = example_file.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    # Binary file
                    pass

    return result


def get_skill_doc(skill_name: str, doc_name: str) -> str:
    """Load a specific documentation file from a skill.

    Args:
        skill_name: Name of the skill.
        doc_name: Name of the doc file (e.g., 'edge_cases.md').

    Returns:
        Content of the documentation file.

    Raises:
        FileNotFoundError: If doc doesn't exist.
    """
    dir_name = _normalize_skill_name(skill_name)
    skills_dir = get_skills_directory()
    doc_path = skills_dir / dir_name / "docs" / doc_name

    if not doc_path.exists():
        raise FileNotFoundError(f"Doc not found: {doc_path}")

    return doc_path.read_text(encoding="utf-8")


def get_skill_script(skill_name: str, script_name: str) -> str:
    """Load a specific script from a skill.

    Args:
        skill_name: Name of the skill.
        script_name: Name of the script file.

    Returns:
        Content of the script file.

    Raises:
        FileNotFoundError: If script doesn't exist.
    """
    dir_name = _normalize_skill_name(skill_name)
    skills_dir = get_skills_directory()
    script_path = skills_dir / dir_name / "scripts" / script_name

    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    return script_path.read_text(encoding="utf-8")


# =============================================================================
# Guardrails and Command Access
# =============================================================================

def get_skill_guardrails(skill_name: str) -> dict[str, list[str]]:
    """Get guardrails (allowed/forbidden actions) for a skill.

    Args:
        skill_name: Name of the skill.

    Returns:
        Dictionary with 'allowed' and 'forbidden' lists.
    """
    skill = load_skill(skill_name)
    skill_md = skill.get("skill_md", "")
    
    guardrails = {"allowed": [], "forbidden": []}
    
    # Parse from skill.md
    in_allowed = False
    in_forbidden = False
    
    for line in skill_md.split("\n"):
        line = line.strip()
        if "### Allowed" in line or "## Allowed" in line:
            in_allowed = True
            in_forbidden = False
        elif "### Forbidden" in line or "## Forbidden" in line:
            in_allowed = False
            in_forbidden = True
        elif line.startswith("##"):
            in_allowed = False
            in_forbidden = False
        elif line.startswith("- ") and in_allowed:
            guardrails["allowed"].append(line[2:])
        elif line.startswith("- ") and in_forbidden:
            guardrails["forbidden"].append(line[2:])
    
    return guardrails


def get_skill_command(skill_name: str) -> dict[str, Any]:
    """Get command specification for a skill.

    Args:
        skill_name: Name of the skill.

    Returns:
        Command specification dictionary.
    """
    metadata = get_skill_metadata(skill_name)
    return {
        "binary": metadata.get("command", {}).get("binary", "skillpack"),
        "subcommand": metadata.get("command", {}).get("subcommand", skill_name),
        "template": metadata.get("command", {}).get("template", f"skillpack {skill_name}"),
        "arguments": metadata.get("arguments", {}),
    }


# =============================================================================
# Export Functions
# =============================================================================

def format_skill_for_llm(skill_name: str, tier: int = 2) -> str:
    """Format skill for LLM consumption.

    Args:
        skill_name: Name of the skill.
        tier: Disclosure tier (1=metadata, 2=+procedure, 3=+everything).

    Returns:
        Formatted string representation.
    """
    if tier == 1:
        skill = get_skill_metadata(skill_name)
    elif tier == 2:
        skill = load_skill(skill_name)
    else:
        skill = load_skill_full(skill_name)

    lines = [
        f"# Skill: {skill.get('name', skill_name)}",
        f"Version: {skill.get('version', '1.0.0')}",
        f"Description: {skill.get('description', 'No description')}",
        f"Tags: {', '.join(skill.get('tags', []))}",
        "",
    ]

    if tier >= 2 and "skill_md" in skill:
        lines.append("## Procedure")
        lines.append(skill["skill_md"])
        lines.append("")

    if tier >= 2:
        if skill.get("available_docs"):
            lines.append(f"Available docs: {', '.join(skill['available_docs'])}")
        if skill.get("available_scripts"):
            lines.append(f"Available scripts: {', '.join(skill['available_scripts'])}")

    return "\n".join(lines)


def export_skills_json(tier: int = 1) -> str:
    """Export all skills as JSON.

    Args:
        tier: Disclosure tier for each skill.

    Returns:
        JSON string with all skills.
    """
    if tier == 1:
        skills_data = list_skills()
    else:
        skills_data = []
        for skill in list_skills():
            name = skill.get("name", skill.get("_directory", ""))
            if name:
                if tier == 2:
                    skills_data.append(load_skill(name))
                else:
                    skills_data.append(load_skill_full(name))

    return json.dumps({"skills": skills_data, "tier": tier}, indent=2, ensure_ascii=False)
