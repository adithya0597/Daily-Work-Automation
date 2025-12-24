# Quality Gate Skill

## When to Use
- Run format, lint, type-check, and tests
- Validate code quality before commit/merge

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| check | boolean | No | Check only, don't modify files |

## Outputs
This skill produces no file output. Results are written to stdout.

## Procedure
1. Run `ruff format` (with --check if check mode)
2. Run `ruff check` (with --fix if not check mode)
3. Run `mypy skillpack/`
4. Run `pytest tests/ -v`

## Example
```bash
# Fix and check
skillpack quality-gate

# Check only (no modifications)
skillpack quality-gate --check
```

## Related Skills
- test-writer - Generate tests for source files
