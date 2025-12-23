# Quality Gate Skill

## When to Use
- Before committing code
- In CI pipeline
- Before creating PR

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| --check | flag | No | Check-only mode (no modifications) |

## Outputs
Console output with pass/fail status

## Procedure
1. **Format** - Run ruff format
2. **Lint** - Run ruff check --fix
3. **Type Check** - Run mypy
4. **Test** - Run pytest

## Guardrails
### Allowed
- Read Python files
- Modify files for formatting (unless --check)
- Run ruff, mypy, pytest

### Forbidden
- Delete files
- Modify non-Python files

## Example
```bash
skillpack quality-gate
skillpack quality-gate --check  # CI mode
```
