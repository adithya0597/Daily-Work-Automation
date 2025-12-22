---
name: sql_refiner
description: Generate SQL queries from natural language questions
tags: [sql, query, postgres, bigquery, snowflake]
activation_triggers:
  - "write sql"
  - "generate query"
  - "sql from question"
version: "0.1.0"
dependencies: []
---

# SQL Query Refiner Skill

## Overview

Generates SQL queries from natural language questions:
- Detects aggregations, conditions, ordering
- Supports multiple SQL dialects
- Generates EXPLAIN query for performance analysis
- Provides query notes with placeholders

## Workflow

1. Parse natural language question
2. Extract entities (aggregations, filters, limits)
3. Generate dialect-specific SQL
4. Generate EXPLAIN query
5. Create notes with usage guidance
6. Write to `./out/sql_refiner/`

## Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--question` | Yes | - | Natural language question |
| `--dialect` | No | postgres | SQL dialect (postgres, bigquery, snowflake) |

## Outputs

```
./out/sql_refiner/
├── query.sql        # Main query
├── explain.sql      # EXPLAIN query
└── query_notes.md   # Usage notes
```

## Error Handling

- Unknown dialect: Returns error with valid options
- Empty question: Generates basic template

## Examples

```bash
# Simple query
skillpack sql-refiner --question "How many active users signed up last 30 days"

# With specific dialect
skillpack sql-refiner --question "Get top 10 orders by amount" --dialect bigquery

# Aggregation query
skillpack sql-refiner --question "What is the average order value per customer"
```

## Related Skills

- `profile-dataset`: Understand data before writing queries
- `schema-diff`: Check schema compatibility
