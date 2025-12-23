# Quality Gate Skill

## When to Use
- Before committing code
- In CI pipeline
- Before creating PR

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| --check | flag | No | Check-only mode (no file modifications) |

## Outputs
Console output with pass/fail status. Exit code 0=pass, 1=fail.

## Procedure
1. **Format** - Run `ruff format`
2. **Lint** - Run `ruff check --fix`
3. **Type Check** - Run `mypy`
4. **Test** - Run `pytest`

## Guardrails

### Allowed
- Read Python files in workspace
- Modify files for formatting (unless --check)
- Run ruff, mypy, pytest commands
- Write to stdout/stderr

### Forbidden
- Delete any files
- Modify files when --check is set
- Modify configuration files
- Execute arbitrary commands

## Preconditions
- [ ] ruff, mypy, pytest installed
- [ ] Python package is importable

## Postconditions
- [ ] All steps completed
- [ ] Exit code reflects result

## Error Handling
| Error | Condition | Recovery |
|-------|-----------|----------|
| ToolNotFound | Tool not installed | pip install {tool} |
| TestFailure | Tests failed | Review test output |
| TypeErrors | Type check failed | Fix type annotations |

## Examples
```bash
skillpack quality-gate           # Fix and test
skillpack quality-gate --check   # CI mode, check only
```

## Related Skills
- **project-scaffolding**: Create project with quality tools
