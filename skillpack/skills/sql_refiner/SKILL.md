# SQL Refiner Skill

## When to Use
- Converting questions to SQL
- Need dialect-specific syntax
- Want query optimization hints

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| question | string | Yes | Natural language question |
| dialect | enum | No | postgres, bigquery, snowflake |

## Outputs
- `query.sql` - Generated SQL query
- `explain.sql` - EXPLAIN statement
- `query_notes.md` - Usage notes

## Procedure
1. **Parse question** - Extract entities, aggregations
2. **Match patterns** - COUNT, SUM, AVG, etc.
3. **Generate SQL** - Dialect-specific syntax
4. **Write outputs** - Save to ./out/

## Guardrails
### Allowed
- Parse natural language
- Generate SQL templates
- Write to ./out/sql_refiner/

### Forbidden
- Execute SQL queries
- Connect to databases

## Example
```bash
skillpack sql-refiner --question "How many active users" --dialect postgres
```
