# Schema Diff Skill

## When to Use
- Compare two schema JSON files
- Generate migration SQL with rollback

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| old | path | Yes | Path to old schema JSON file |
| new | path | Yes | Path to new schema JSON file |
| table | string | No | Table name for migration (default: table_name) |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| migration.sql | SQL | Forward and rollback migration statements |
| migration.md | markdown | Migration notes and impact assessment |

## Example
```bash
skillpack schema-diff --old v1_schema.json --new v2_schema.json --table users
```

## Related Skills
- data-quality - Validate data against schema
