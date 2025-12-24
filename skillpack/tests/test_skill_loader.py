"""Tests for skill loader with progressive disclosure."""

from pathlib import Path

import pytest

from skillpack.utils.skill_loader import (
    export_skills_json,
    format_skill_for_llm,
    get_skill_guardrails,
    get_skill_metadata,
    list_skills,
    load_skill,
    load_skill_full,
)


def test_list_skills_returns_list() -> None:
    """Test that list_skills returns a list of skills."""
    skills = list_skills()
    assert isinstance(skills, list)
    assert len(skills) >= 1


def test_list_skills_has_metadata_fields() -> None:
    """Test that each skill has required metadata fields."""
    skills = list_skills()
    for skill in skills:
        # New format uses flat structure (not nested under 'skill')
        assert "description" in skill or "name" in skill
        assert "_directory" in skill


def test_get_skill_metadata() -> None:
    """Test getting metadata for a specific skill."""
    metadata = get_skill_metadata("profile-dataset")
    assert metadata is not None
    assert "description" in metadata


def test_load_skill_tier2() -> None:
    """Test loading skill with procedure (Tier 2)."""
    skill = load_skill("profile-dataset")
    assert skill is not None
    assert "_tier" in skill
    assert skill["_tier"] == 2
    assert "skill_md" in skill
    assert "available_docs" in skill
    assert "available_scripts" in skill


def test_load_skill_full_tier3() -> None:
    """Test loading full skill content (Tier 3)."""
    skill = load_skill_full("profile-dataset")
    assert skill is not None
    assert skill["_tier"] == 3
    assert "docs" in skill
    assert "scripts" in skill
    # profile_dataset has edge_cases.md and profile_csv.py
    assert "edge_cases.md" in skill.get("docs", {})
    assert "profile_csv.py" in skill.get("scripts", {})


def test_load_skill_not_found() -> None:
    """Test that loading non-existent skill raises error."""
    with pytest.raises(FileNotFoundError):
        load_skill("nonexistent-skill")


def test_format_skill_for_llm_tier1() -> None:
    """Test LLM-formatted output at Tier 1."""
    output = format_skill_for_llm("profile-dataset", tier=1)
    assert "# Skill: profile-dataset" in output
    assert "Description:" in output


def test_format_skill_for_llm_tier2() -> None:
    """Test LLM-formatted output at Tier 2."""
    output = format_skill_for_llm("profile-dataset", tier=2)
    assert "# Skill: profile-dataset" in output
    assert "## Procedure" in output
    assert "Available docs:" in output or "Available scripts:" in output


def test_export_skills_json() -> None:
    """Test JSON export of all skills."""
    import json

    output = export_skills_json()
    data = json.loads(output)
    assert "skills" in data
    assert "tier" in data
    assert isinstance(data["skills"], list)


def test_get_skill_guardrails() -> None:
    """Test extracting guardrails from skill.md."""
    guardrails = get_skill_guardrails("profile-dataset")
    assert "allowed" in guardrails
    assert "forbidden" in guardrails
    # profile-dataset has guardrails defined
    assert len(guardrails["allowed"]) > 0
    assert len(guardrails["forbidden"]) > 0


def test_progressive_disclosure_efficiency() -> None:
    """Test that Tier 1 is more compact than Tier 3."""
    metadata = get_skill_metadata("profile-dataset")
    full = load_skill_full("profile-dataset")
    
    # Full should have more keys than metadata
    assert len(full) > len(metadata)
    
    # Full should have docs and scripts
    assert "docs" in full
    assert "scripts" in full


# =============================================================================
# Dependency Validation Tests
# =============================================================================

def test_skill_exists() -> None:
    """Test skill_exists returns correct values."""
    from skillpack.utils.skill_loader import skill_exists
    
    assert skill_exists("profile-dataset") is True
    assert skill_exists("nonexistent-skill") is False


def test_get_skill_dependencies() -> None:
    """Test getting dependencies from a skill."""
    from skillpack.utils.skill_loader import get_skill_dependencies
    
    # data-quality declares profile-dataset as dependency
    deps = get_skill_dependencies("data-quality")
    assert isinstance(deps, list)
    assert "profile-dataset" in deps


def test_validate_dependencies_valid() -> None:
    """Test validating a skill with valid dependencies."""
    from skillpack.utils.skill_loader import validate_dependencies
    
    result = validate_dependencies("data-quality")
    assert result["valid"] is True
    assert "profile-dataset" in result["dependencies"]
    assert len(result["missing"]) == 0


def test_validate_all_dependencies() -> None:
    """Test validating all skills."""
    from skillpack.utils.skill_loader import validate_all_dependencies
    
    result = validate_all_dependencies()
    assert result["total_skills"] == 16
    assert "details" in result


def test_get_dependency_graph() -> None:
    """Test building the dependency graph."""
    from skillpack.utils.skill_loader import get_dependency_graph
    
    graph = get_dependency_graph()
    assert len(graph) == 16
    assert "data-quality" in graph
    assert "profile-dataset" in graph["data-quality"]


def test_get_reverse_dependencies() -> None:
    """Test getting skills that depend on a given skill."""
    from skillpack.utils.skill_loader import get_reverse_dependencies
    
    # profile-dataset is a dependency of data-quality and dbt-generator
    dependents = get_reverse_dependencies("profile-dataset")
    assert "data-quality" in dependents
