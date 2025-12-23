# SQL Refiner Skill

## When to Use
- Converting questions to SQL
- Need dialect-specific syntax
- Want query optimization hints

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| question | string | Yes | Natural language question |
| dialect | enum | No | postgres, bigquery, snowflake (default: postgres) |

## Outputs
- `./out/sql_refiner/query.sql` - Generated SQL query
- `./out/sql_refiner/explain.sql` - EXPLAIN statement
- `./out/sql_refiner/query_notes.md` - Usage notes

## Procedure
1. **Parse question** - Extract entities, aggregations
2. **Match patterns** - COUNT, SUM, AVG, TOP, etc.
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
- Access credentials
- Modify any existing files

## Preconditions
- [ ] Question contains queryable entities

## Postconditions
- [ ] query.sql is valid SQL syntax
- [ ] explain.sql wraps query correctly

## Error Handling
| Error | Condition | Recovery |
|-------|-----------|----------|
| NoEntitiesFound | Question too vague | Be more specific |
| UnsupportedDialect | Unknown dialect | Use postgres/bigquery/snowflake |

## Supported Patterns
- Count: "how many", "count of"
- Sum: "total", "sum of"
- Average: "average", "mean"
- Top N: "top 10", "first 5"

## Dialect Differences
| Feature | PostgreSQL | BigQuery | Snowflake |
|---------|------------|----------|-----------|
| LIMIT | `LIMIT n` | `LIMIT n` | `LIMIT n` |
| Case | lowercase | lowercase | UPPERCASE |

## Examples
```bash
skillpack sql-refiner --question "How many active users"
skillpack sql-refiner --question "Top 10 orders" --dialect bigquery
```

## Related Skills
- **profile-dataset**: Understand data before querying
- **schema-diff**: Track schema changes
