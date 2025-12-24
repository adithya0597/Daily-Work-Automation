# Sql Refiner Skill

## When to Use
- Generate SQL queries from natural language questions.
- Automate sql refiner generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| question | string | No | Natural language question to convert to SQL |
| dialect | string | No | SQL dialect (default: postgres) |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| output.md | file | Generated output |

## Example
```bash
skillpack sql-refiner --name example
```

## Related Skills
- Check skillpack --help for related skills
