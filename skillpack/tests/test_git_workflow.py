"""Tests for git-workflow skill."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from skillpack.skills.git_workflow import (
    create_branch,
    format_commit,
    generate_pr_template,
    slugify,
)


def test_slugify_basic() -> None:
    """Test slugify converts text correctly."""
    assert slugify("Add User Auth") == "add-user-auth"
    assert slugify("Fix bug #123") == "fix-bug-123"
    assert slugify("  spaces  ") == "spaces"


def test_create_branch_feature() -> None:
    """Test creating a feature branch."""
    result = create_branch(
        branch_type="feature",
        description="Add User Authentication",
    )
    assert result["success"]
    assert result["branch_name"] == "feature/add-user-authentication"


def test_create_branch_with_issue() -> None:
    """Test creating a branch with issue number."""
    result = create_branch(
        branch_type="feature",
        description="login page",
        issue="PROJ-123",
    )
    assert result["success"]
    assert result["branch_name"] == "feature/PROJ-123-login-page"


def test_create_branch_bugfix() -> None:
    """Test creating a bugfix branch."""
    result = create_branch(
        branch_type="bugfix",
        description="Fix null pointer",
    )
    assert result["success"]
    assert "bugfix/" in result["branch_name"]


def test_format_commit_simple() -> None:
    """Test formatting a simple commit."""
    result = format_commit(
        commit_type="feat",
        description="add login functionality",
    )
    assert result["success"]
    assert result["commit_message"] == "feat: add login functionality"


def test_format_commit_with_scope() -> None:
    """Test formatting a commit with scope."""
    result = format_commit(
        commit_type="fix",
        scope="auth",
        description="handle null tokens",
    )
    assert result["success"]
    assert result["commit_message"] == "fix(auth): handle null tokens"


def test_format_commit_breaking() -> None:
    """Test formatting a breaking change commit."""
    result = format_commit(
        commit_type="feat",
        description="new API",
        breaking=True,
    )
    assert result["success"]
    assert "!" in result["commit_message"]


def test_generate_pr_template() -> None:
    """Test generating a PR template."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Patch write_text to use temp directory
        with patch("skillpack.skills.git_workflow.write_text") as mock_write:
            mock_write.return_value = Path(tmpdir) / "PR_TEMPLATE.md"
            
            result = generate_pr_template(
                title="Add User Authentication",
                branch="feature/add-auth",
            )
            assert result["success"]
            mock_write.assert_called_once()
