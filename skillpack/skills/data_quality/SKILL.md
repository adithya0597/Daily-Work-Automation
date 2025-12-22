---
name: data_quality
description: Generate Pandera validation schemas for data quality
tags: [data, validation, pandera, quality]
activation_triggers:
  - "validate data"
  - "create schema"
  - "data quality"
version: "0.1.0"
dependencies: [pandera, pandas]
---

# Data Quality Skill

## Overview

Generates Pandera validation schemas from configuration:
- Creates `schema.py` with DataFrame schema
- Creates `run_validation.py` runner script
- Supports various column types and checks

## Workflow

1. Read configuration (YAML or JSON)
2. Generate Pandera schema with columns and checks
3. Generate validation runner script
4. Write to `./out/data_quality/`

## Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--config` | No | - | Path to config file (generates example if not provided) |

### Config Format

```yaml
name: UserSchema
columns:
  - name: id
    type: integer
    nullable: false
    unique: true
    checks:
      - type: min
        value: 1
  - name: email
    type: string
    nullable: false
    checks:
      - type: regex
        pattern: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
  - name: age
    type: integer
    nullable: true
    checks:
      - type: between
        min: 0
        max: 150
```

## Outputs

```
./out/data_quality/
├── schema.py           # Pandera schema
└── run_validation.py   # Runner script
```

## Error Handling

- Invalid config: Returns parsing error
- Unknown types: Maps to string

## Examples

```bash
# Generate example schema
skillpack data-quality

# Generate from config
skillpack data-quality --config schema_config.yaml

# Run validation
python ./out/data_quality/run_validation.py data.csv
```

## Related Skills

- `profile-dataset`: Profile data before creating schema
- `dbt-generator`: Add tests to dbt models
