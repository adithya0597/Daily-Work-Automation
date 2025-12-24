"""Tests for Phase 1 productivity skills."""

import tempfile
from pathlib import Path

import pytest


class TestNotebookToPackage:
    """Tests for notebook-to-package skill."""

    def test_notebook_to_package_main(self):
        """Test converting a notebook to package."""
        from skillpack.skills.notebook_to_package import notebook_to_package_main

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a minimal notebook
            notebook_path = Path(tmpdir) / "test_notebook.ipynb"
            notebook_path.write_text("""{
                "cells": [
                    {"cell_type": "code", "source": ["def hello():\\n", "    return 'world'"], "metadata": {}},
                    {"cell_type": "markdown", "source": ["# Title"]}
                ],
                "metadata": {},
                "nbformat": 4
            }""")

            output_dir = Path(tmpdir) / "output"
            result = notebook_to_package_main(
                notebook_path=notebook_path,
                package_name="mypackage",
                output_dir=output_dir,
            )

            assert result["success"] is True
            assert "mypackage" in result["package_name"]


class TestTestWriter:
    """Tests for test-writer skill."""

    def test_test_writer_main(self):
        """Test generating tests from source."""
        from skillpack.skills.test_writer import test_writer_main

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a source file
            source_path = Path(tmpdir) / "sample.py"
            source_path.write_text("""
def add(a, b):
    return a + b

class Calculator:
    def multiply(self, x, y):
        return x * y
""")

            output_dir = Path(tmpdir) / "output"
            result = test_writer_main(
                source_path=source_path,
                output_dir=output_dir,
            )

            assert result["success"] is True


class TestRefactorSkill:
    """Tests for refactor-skill skill."""

    def test_refactor_skill_main(self):
        """Test analyzing code for refactoring."""
        from skillpack.skills.refactor_skill import refactor_skill_main

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a source file with some complexity
            source_path = Path(tmpdir) / "complex.py"
            source_path.write_text("""
def complex_function(x, y, z):
    if x > 0:
        if y > 0:
            if z > 0:
                return x + y + z
            else:
                return x + y
        else:
            return x
    else:
        return 0

def simple_function():
    return 42
""")

            output_dir = Path(tmpdir) / "output"
            result = refactor_skill_main(
                source_path=source_path,  # Correct param name
                threshold=3,  # Correct param name (not complexity_threshold)
                output_dir=output_dir,
            )

            assert result["success"] is True
