# Data Quality Skill

## When to Use
- Generate Pandera validation schemas
- Create data validation scripts

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| config | path | No | Config file (YAML/JSON). Generates example if not provided. |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| schema.py | python | Pandera DataFrameSchema definition |
| run_validation.py | python | Runner script for validation |

## Example
```bash
# Generate from config
skillpack data-quality --config schema_config.yaml

# Generate example
skillpack data-quality
```

## Usage
```bash
python run_validation.py data.csv
```

## Related Skills
- profile-dataset - Profile data before creating schema
