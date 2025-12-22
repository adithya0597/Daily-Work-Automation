"""Project Scaffolding Skill - Generate new project skeletons."""

import argparse
from pathlib import Path
from typing import Any

from skillpack.utils.logging import get_logger
from skillpack.utils.output import get_output_dir, write_text

SKILL_NAME = "project_scaffolding"

# Templates for generated files
TEMPLATES: dict[str, str] = {
    "pyproject.toml": '''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{name}"
version = "0.1.0"
description = "{description}"
readme = "README.md"
license = {{text = "MIT"}}
requires-python = ">=3.11"

dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
]

[tool.ruff]
target-version = "py311"
line-length = 100

[tool.mypy]
python_version = "3.11"
warn_return_any = true
disallow_untyped_defs = true
''',
    "README.md": '''# {name}

{description}

## Quick Start

```bash
pip install -e ".[dev]"
```

## Development

```bash
# Run tests
pytest tests/

# Lint
ruff check src/

# Type check
mypy src/
```

## License

MIT
''',
    ".gitignore": '''__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.env
.venv/
''',
    ".env.example": '''# Environment variables for {name}
# Copy to .env and fill in values
''',
    "src/__init__.py": '''"""{name} - {description}"""

__version__ = "0.1.0"
''',
    "src/main.py": '''"""Main module for {name}."""


def main() -> None:
    """Entry point."""
    print("Hello from {name}!")


if __name__ == "__main__":
    main()
''',
    "tests/__init__.py": '''"""Tests for {name}."""
''',
    "tests/test_main.py": '''"""Tests for main module."""

from src.main import main


def test_main(capsys):
    """Test main function runs without error."""
    main()
    captured = capsys.readouterr()
    assert "{name}" in captured.out
''',
    ".github/workflows/ci.yml": '''name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - run: ruff check src/ tests/
      - run: mypy src/
      - run: pytest tests/
''',
    ".vscode/settings.json": '''{{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.analysis.typeCheckingMode": "basic"
}}
''',
    ".pre-commit-config.yaml": '''repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
''',
}


def generate_project(
    name: str,
    description: str = "A new Python project",
    base_dir: str = "./out",
) -> Path:
    """Generate a new project skeleton.

    Args:
        name: Project name.
        description: Project description.
        base_dir: Base output directory.

    Returns:
        Path to the generated project directory.
    """
    logger = get_logger()
    output_dir = get_output_dir(SKILL_NAME, base_dir)
    project_dir = output_dir / name

    logger.info(f"Generating project skeleton: {name}")

    for file_path, template in sorted(TEMPLATES.items()):
        content = template.format(name=name, description=description)

        # Handle nested directories
        full_path = project_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
        logger.debug(f"  Created: {file_path}")

    logger.info(f"Project generated at: {project_dir}")
    return project_dir


def handler(args: argparse.Namespace) -> int:
    """Handle the project-scaffolding command."""
    try:
        project_dir = generate_project(
            name=args.name,
            description=args.description,
        )
        print(f"✅ Project generated: {project_dir}")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def register_parser(subparsers: Any) -> None:
    """Register the project-scaffolding subcommand."""
    parser = subparsers.add_parser(
        "project-scaffolding",
        help="Generate a new project skeleton",
        description="Creates a new mini-project with pyproject.toml, README, tests, CI, etc.",
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Name of the project to create",
    )
    parser.add_argument(
        "--description",
        default="A new Python project",
        help="Project description (default: 'A new Python project')",
    )
    parser.set_defaults(handler=handler)
