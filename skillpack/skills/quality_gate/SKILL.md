---
name: quality_gate
description: Run format + lint + type-check + tests in one command
tags: [quality, lint, format, test, ci]
activation_triggers:
  - "run quality checks"
  - "lint and test"
  - "check code quality"
version: "0.1.0"
dependencies: [ruff, mypy, pytest]
---

# Quality Gate Skill

## Overview

Runs a comprehensive quality gate that includes:
1. **Format**: Auto-format code with ruff
2. **Lint**: Check for code issues with ruff
3. **Type Check**: Validate types with mypy
4. **Tests**: Run pytest test suite

## Workflow

1. Format code (or check formatting in `--check` mode)
2. Run linter (auto-fix in normal mode)
3. Run type checker
4. Run test suite
5. Report overall status

## Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--check` | No | false | Check only, don't modify files |

## Outputs

- Console output with pass/fail status for each step
- Exit code 0 if all checks pass, non-zero otherwise

## Error Handling

- Individual check failures don't stop subsequent checks
- All failures are reported at the end
- Exit code reflects the last failing step

## Examples

```bash
# Run full quality gate (with auto-fix)
skillpack quality-gate

# Check only (CI mode)
skillpack quality-gate --check
```

## Related Skills

- `project-scaffolding`: Create a project with pre-configured quality tools
- `pr-summary`: Summarize changes before submitting
