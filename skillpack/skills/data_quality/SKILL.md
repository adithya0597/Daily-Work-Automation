# Data Quality Skill

## When to Use
- Creating data validation rules
- Before ETL pipelines
- After profiling a dataset

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| config_path | file_path | No | Schema config file |

## Outputs
- `schema.py` - Pandera schema definition
- `run_validation.py` - Validation runner

## Procedure
1. **Load config** - Parse YAML/JSON or use example
2. **Generate schema** - Create Pandera DataFrameSchema
3. **Create runner** - Script to validate CSV files
4. **Write outputs** - Save to ./out/

## Guardrails
### Allowed
- Read config file
- Generate Python code
- Write to ./out/data_quality/

### Forbidden
- Execute generated schema
- Access data files

## Example
```bash
skillpack data-quality --config schema_config.yaml
```
