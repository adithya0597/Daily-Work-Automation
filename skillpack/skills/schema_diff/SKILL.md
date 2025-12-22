---
name: schema_diff
description: Compare database schemas and generate migration scripts
tags: [schema, migration, database, diff]
activation_triggers:
  - "compare schemas"
  - "generate migration"
  - "schema diff"
version: "0.1.0"
dependencies: []
---

# Schema Diff Skill

## Overview

Compares two schema definitions and generates:
- Migration SQL with forward and rollback statements
- Impact assessment with backfill requirements
- Documentation of all changes

## Workflow

1. Load old and new schema JSON files
2. Compare columns (added, removed, modified)
3. Detect PK changes
4. Generate migration SQL
5. Generate impact notes
6. Write to `./out/schema_diff/`

## Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--old` | Yes | - | Path to old schema JSON |
| `--new` | Yes | - | Path to new schema JSON |
| `--table` | No | "table_name" | Table name for migration |

### Schema Format

```json
{
  "columns": [
    {"name": "id", "type": "INTEGER", "nullable": false, "pk": true},
    {"name": "email", "type": "VARCHAR(255)", "nullable": false},
    {"name": "created_at", "type": "TIMESTAMP", "nullable": true}
  ]
}
```

## Outputs

```
./out/schema_diff/
├── migration.sql   # Forward + rollback SQL
└── migration.md    # Impact documentation
```

## Error Handling

- Missing files: Returns error with path
- Invalid JSON: Returns parsing error

## Examples

```bash
# Compare schemas
skillpack schema-diff --old schema_v1.json --new schema_v2.json

# With table name
skillpack schema-diff --old v1.json --new v2.json --table users
```

## Related Skills

- `pr-summary`: Include migration in PR summary
- `dbt-generator`: Update dbt models for schema changes
