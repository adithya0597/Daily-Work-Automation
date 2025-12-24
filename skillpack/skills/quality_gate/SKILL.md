# Quality Gate Skill

## When to Use
- Run format + lint + type-check + tests.
- Automate quality gate generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| check | string | No | Check only, don |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| output.md | file | Generated output |

## Example
```bash
skillpack quality-gate --name example
```

## Related Skills
- Check skillpack --help for related skills
