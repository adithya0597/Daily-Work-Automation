---
name: dbt_generator
description: Generate dbt models, tests, and documentation
tags: [dbt, models, sql, data]
activation_triggers:
  - "generate dbt"
  - "create dbt models"
  - "dbt project"
version: "0.1.0"
dependencies: []
---

# dbt Generator Skill

## Overview

Generates dbt project files from configuration:
- Staging models with source references
- Mart models with transformations
- schema.yml with tests and documentation
- Documentation blocks

## Workflow

1. Read configuration (YAML or JSON)
2. Generate staging models for each source
3. Generate mart models with aggregations
4. Create schema.yml with all models
5. Generate documentation block
6. Write to `./out/dbt_generator/`

## Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--config` | No | - | Path to config file (generates example if not provided) |

### Config Format

```yaml
project_name: My dbt Project
sources:
  - source_name: raw
    table_name: users
    columns:
      - name: id
        alias: user_id
        tests: [unique, not_null]
      - name: email
        tests: [unique]
models:
  - name: mart_user_summary
    description: User summary mart
    refs:
      - name: stg_users
        alias: users
    columns:
      - name: user_id
        source: users
    aggregations:
      - function: COUNT
        column: "*"
        alias: total_users
```

## Outputs

```
./out/dbt_generator/
└── models/
    ├── staging/
    │   └── stg_<table>.sql
    ├── marts/
    │   └── <mart_name>.sql
    ├── schema.yml
    └── docs.md
```

## Error Handling

- Invalid config: Returns parsing error
- Missing required fields: Uses defaults

## Examples

```bash
# Generate example project
skillpack dbt-generator

# Generate from config
skillpack dbt-generator --config dbt_config.yaml
```

## Related Skills

- `profile-dataset`: Profile data before modeling
- `data-quality`: Add Pandera validation
- `schema-diff`: Track schema changes
