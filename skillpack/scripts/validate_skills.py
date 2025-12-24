#!/usr/bin/env python3
"""Validate skill structure and consistency.

This script validates that all skills in skillpack follow the required structure.
Run it before committing changes or adding new skills.

Usage:
    python scripts/validate_skills.py [--skill SKILL_NAME]
"""

import argparse
import sys
from pathlib import Path

# Add skillpack to path
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

from skillpack.utils.skill_loader import (
    get_skill_guardrails,
    list_skills,
    load_skill,
    validate_all_dependencies,
)


def validate_skill_structure(skill_name: str, skill_dir: Path) -> list[str]:
    """Validate a single skill's structure."""
    errors = []
    warnings = []

    # Required files
    if not (skill_dir / "metadata.yaml").exists():
        errors.append(f"{skill_name}: Missing metadata.yaml")
    if not (skill_dir / "skill.md").exists():
        errors.append(f"{skill_name}: Missing skill.md")

    # Recommended directories
    if not (skill_dir / "docs").exists():
        warnings.append(f"{skill_name}: Missing docs/ directory")
    if not (skill_dir / "scripts").exists():
        warnings.append(f"{skill_name}: Missing scripts/ directory")
    if not (skill_dir / "examples").exists():
        warnings.append(f"{skill_name}: Missing examples/ directory")

    return errors, warnings


def validate_skill_content(skill_name: str) -> list[str]:
    """Validate skill metadata and content."""
    errors = []
    warnings = []

    try:
        skill = load_skill(skill_name)

        # Required metadata
        if not skill.get("name"):
            errors.append(f"{skill_name}: Missing 'name' in metadata.yaml")
        if not skill.get("version"):
            errors.append(f"{skill_name}: Missing 'version' in metadata.yaml")
        if not skill.get("description"):
            errors.append(f"{skill_name}: Missing 'description' in metadata.yaml")
        if not skill.get("tags"):
            warnings.append(f"{skill_name}: Missing 'tags' in metadata.yaml")
        if not skill.get("triggers"):
            warnings.append(f"{skill_name}: Missing 'triggers' in metadata.yaml")

        # Command specification
        if "command" not in skill:
            errors.append(f"{skill_name}: Missing 'command' in metadata.yaml")
        elif not skill.get("command", {}).get("template"):
            warnings.append(f"{skill_name}: Missing command template")

        # skill.md content
        if not skill.get("skill_md"):
            errors.append(f"{skill_name}: Empty or missing skill.md")
        else:
            skill_md = skill["skill_md"]
            if "## Guardrails" not in skill_md:
                errors.append(f"{skill_name}: Missing Guardrails section in skill.md")
            if "## Procedure" not in skill_md:
                warnings.append(f"{skill_name}: Missing Procedure section in skill.md")
            if "## Error Handling" not in skill_md:
                warnings.append(f"{skill_name}: Missing Error Handling in skill.md")

        # Guardrails
        guardrails = get_skill_guardrails(skill_name)
        if not guardrails.get("allowed"):
            errors.append(f"{skill_name}: No allowed actions in guardrails")
        if not guardrails.get("forbidden"):
            errors.append(f"{skill_name}: No forbidden actions in guardrails")

    except Exception as e:
        errors.append(f"{skill_name}: Error loading skill: {e}")

    return errors, warnings


def validate_all_skills() -> tuple[list[str], list[str]]:
    """Validate all skills."""
    all_errors = []
    all_warnings = []

    skills_dir = REPO_ROOT / "skills"

    print("=" * 60)
    print("Skillpack Validation")
    print("=" * 60)
    print()

    skills = list_skills()
    print(f"Found {len(skills)} skills")
    print()

    for skill in skills:
        skill_name = skill.get("name", skill.get("_directory", ""))
        if not skill_name:
            continue

        dir_name = skill_name.replace("-", "_")
        skill_dir = skills_dir / dir_name

        print(f"Validating: {skill_name}")

        # Structure validation
        errors, warnings = validate_skill_structure(skill_name, skill_dir)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

        # Content validation
        errors, warnings = validate_skill_content(skill_name)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    # Dependency validation
    print()
    print("Validating dependencies...")
    dep_result = validate_all_dependencies()
    if not dep_result["valid"]:
        all_errors.extend(dep_result["warnings"])

    return all_errors, all_warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate skillpack skills")
    parser.add_argument("--skill", help="Validate a specific skill only")
    args = parser.parse_args()

    if args.skill:
        # Validate single skill
        skill_name = args.skill
        dir_name = skill_name.replace("-", "_")
        skill_dir = REPO_ROOT / "skills" / dir_name

        errors1, warnings1 = validate_skill_structure(skill_name, skill_dir)
        errors2, warnings2 = validate_skill_content(skill_name)

        errors = errors1 + errors2
        warnings = warnings1 + warnings2
    else:
        # Validate all
        errors, warnings = validate_all_skills()

    # Print results
    print()
    print("=" * 60)
    print("Results")
    print("=" * 60)

    if warnings:
        print()
        print(f"⚠️  {len(warnings)} Warnings:")
        for warning in warnings:
            print(f"   - {warning}")

    if errors:
        print()
        print(f"❌ {len(errors)} Errors:")
        for error in errors:
            print(f"   - {error}")
        print()
        print("VALIDATION FAILED")
        return 1

    print()
    print("✅ All validations passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
