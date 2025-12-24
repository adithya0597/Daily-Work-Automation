# Schema Diff Skill

## When to Use
- Compare schemas and generate migrations.
- Automate schema diff generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| old | string | No | Path to old schema JSON file |
| new | string | No | Path to new schema JSON file |
| table | string | No | Table name for the migration (default: table_name) |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| output.md | file | Generated output |

## Example
```bash
skillpack schema-diff --name example
```

## Related Skills
- Check skillpack --help for related skills
