"""Tests for project_scaffolding skill."""

import shutil
from pathlib import Path

import pytest

from skillpack.skills.project_scaffolding import generate_project


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    """Create a temporary output directory."""
    return tmp_path / "out"


def test_generate_project_creates_files(output_dir: Path) -> None:
    """Test that generate_project creates all expected files."""
    project_dir = generate_project(
        name="testproject",
        description="A test project",
        base_dir=str(output_dir),
    )

    # Check project directory exists
    assert project_dir.exists()
    assert project_dir.name == "testproject"

    # Check required files exist
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / "README.md").exists()
    assert (project_dir / ".gitignore").exists()
    assert (project_dir / "src" / "__init__.py").exists()
    assert (project_dir / "tests" / "test_main.py").exists()


def test_generate_project_content(output_dir: Path) -> None:
    """Test that generated files have correct content."""
    project_dir = generate_project(
        name="myapp",
        description="My awesome app",
        base_dir=str(output_dir),
    )

    # Check pyproject.toml content
    pyproject = (project_dir / "pyproject.toml").read_text()
    assert 'name = "myapp"' in pyproject

    # Check README content
    readme = (project_dir / "README.md").read_text()
    assert "# myapp" in readme
    assert "My awesome app" in readme
