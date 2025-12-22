---
name: project_scaffolding
description: Generate new Python project skeletons with best practices
tags: [scaffolding, project, python, cli]
activation_triggers:
  - "create new project"
  - "scaffold project"
  - "initialize project"
version: "0.1.0"
dependencies: []
---

# Project Scaffolding Skill

## Overview

Generates a complete Python project skeleton with modern best practices including:
- `pyproject.toml` with proper configuration
- Pre-configured development tools (ruff, mypy, pytest)
- GitHub Actions CI workflow
- VS Code settings
- Pre-commit hooks

## Workflow

1. User provides project name and optional description
2. Skill creates output directory: `./out/project_scaffolding/<name>/`
3. All template files are generated with proper formatting
4. User can copy/move the generated project to desired location

## Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--name` | Yes | - | Project name |
| `--description` | No | "A new Python project" | Project description |

## Outputs

```
./out/project_scaffolding/<name>/
├── pyproject.toml
├── README.md
├── .gitignore
├── .env.example
├── .pre-commit-config.yaml
├── .github/workflows/ci.yml
├── .vscode/settings.json
├── src/
│   ├── __init__.py
│   └── main.py
└── tests/
    ├── __init__.py
    └── test_main.py
```

## Error Handling

- If output directory already exists, files will be overwritten
- Invalid characters in project name may cause issues

## Examples

```bash
# Create a simple project
skillpack project-scaffolding --name myapp

# Create with custom description
skillpack project-scaffolding --name analytics-service --description "Data analytics service"
```

## Related Skills

- `quality-gate`: Run quality checks on the generated project
- `pr-summary`: Generate PR summary when submitting changes
