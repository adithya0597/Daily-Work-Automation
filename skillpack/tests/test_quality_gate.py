"""Tests for quality_gate skill."""

import pytest

from skillpack.skills.quality_gate import run_command


def test_run_command_success() -> None:
    """Test that run_command works for simple commands."""
    code, stdout, stderr = run_command(["echo", "hello"])
    # On some systems echo returns 0
    assert code == 0 or "hello" in stdout


def test_run_command_not_found() -> None:
    """Test that run_command handles missing commands."""
    code, stdout, stderr = run_command(["nonexistent_command_12345"])
    assert code != 0
    assert "not found" in stderr.lower() or code == 1


def test_run_command_with_args() -> None:
    """Test run_command with arguments."""
    code, stdout, stderr = run_command(["python", "--version"])
    assert code == 0
    assert "Python" in stdout or "Python" in stderr
