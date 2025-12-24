# Dbt Generator Skill

## When to Use
- Generate dbt models and tests from configuration
- Create staging and mart models

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| config | path | No | Path to config file (YAML/JSON). If not provided, generates example. |

## Outputs
| Directory | Description |
|-----------|-------------|
| models/staging/ | Staging model SQL files (stg_*.sql) |
| models/marts/ | Mart model SQL files |
| models/schema.yml | Column definitions and tests |
| models/docs.md | Documentation blocks |

## Example
```bash
# Generate with config
skillpack dbt-generator --config config.yaml

# Generate example (no config)
skillpack dbt-generator
```

## Related Skills
- profile-dataset - Profile data to inform dbt models
- data-quality - Generate validation schemas
