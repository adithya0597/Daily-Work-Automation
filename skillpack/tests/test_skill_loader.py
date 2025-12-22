"""Tests for skill loader and list-skills command."""

from pathlib import Path

import pytest

from skillpack.utils.skill_loader import (
    export_skills_json,
    format_skill_for_llm,
    list_skills,
    load_skill,
)


def test_list_skills_returns_list() -> None:
    """Test that list_skills returns a list of skills."""
    skills = list_skills()
    assert isinstance(skills, list)
    # Should have at least some skills
    assert len(skills) >= 1


def test_list_skills_has_required_fields() -> None:
    """Test that each skill has required metadata."""
    skills = list_skills()
    for skill in skills:
        assert "name" in skill
        assert "version" in skill
        assert "description" in skill


def test_load_skill_profile_dataset() -> None:
    """Test loading a specific skill."""
    skill = load_skill("profile-dataset")
    assert skill is not None
    assert "skill" in skill
    assert skill["skill"]["name"] == "profile-dataset"


def test_load_skill_not_found() -> None:
    """Test that loading non-existent skill raises error."""
    with pytest.raises(FileNotFoundError):
        load_skill("nonexistent-skill")


def test_format_skill_for_llm() -> None:
    """Test LLM-formatted output."""
    output = format_skill_for_llm("profile-dataset")
    assert "# Skill: profile-dataset" in output
    assert "ALLOWED:" in output
    assert "FORBIDDEN:" in output


def test_export_skills_json() -> None:
    """Test JSON export of all skills."""
    import json

    output = export_skills_json()
    data = json.loads(output)
    assert "skills" in data
    assert isinstance(data["skills"], list)


def test_skill_has_guardrails() -> None:
    """Test that skills have guardrails defined."""
    skill = load_skill("profile-dataset")
    guardrails = skill.get("guardrails", {})
    assert "allowed" in guardrails
    assert "forbidden" in guardrails
    assert len(guardrails["forbidden"]) > 0


def test_skill_has_examples() -> None:
    """Test that skills have examples defined."""
    skill = load_skill("profile-dataset")
    examples = skill.get("examples", [])
    assert len(examples) > 0
    assert "command" in examples[0]
