# SQL Refiner Skill

## When to Use
- Generate SQL queries from natural language questions
- Convert questions to dialect-specific SQL

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| question | string | Yes | Natural language question to convert to SQL |
| dialect | string | No | SQL dialect: postgres, bigquery, or snowflake (default: postgres) |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| query.sql | SQL | Generated query template |
| explain.sql | SQL | EXPLAIN plan query |
| query_notes.md | markdown | Analysis and tips |

## Example
```bash
skillpack sql-refiner --question "How many active users in the last 30 days?" --dialect postgres
```

## Related Skills
- dbt-generator - Generate dbt models
- data-quality - Validate query results
