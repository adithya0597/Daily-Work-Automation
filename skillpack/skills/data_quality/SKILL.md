# Data Quality Skill

## When to Use
- Creating data validation rules
- Before ETL pipelines
- After profiling a dataset

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| config_path | file_path | No | Schema configuration YAML |

## Outputs
- `./out/data_quality/schema.py` - Pandera schema definition
- `./out/data_quality/run_validation.py` - Validation runner

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
- Access data files directly
- Modify input config
- Delete any files

## Preconditions
- [ ] Config file is valid YAML (if provided)
- [ ] pandera is available

## Postconditions
- [ ] schema.py is valid Python
- [ ] run_validation.py is executable

## Error Handling
| Error | Condition | Recovery |
|-------|-----------|----------|
| ConfigError | Invalid YAML | Fix YAML syntax |
| ColumnNotFound | Column in config missing | Verify config matches data |

## Config Schema
```yaml
columns:
  - name: column_name
    dtype: string|integer|float|boolean
    nullable: true|false
    unique: true|false
    checks:
      - min_value: 0
      - max_value: 100
      - isin: [a, b, c]
```

## Examples
```bash
skillpack data-quality                        # Use example config
skillpack data-quality --config schema.yaml   # Use custom config
```

## Related Skills
- **profile-dataset**: Generate profile to inform schema
