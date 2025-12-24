# Profile Dataset Skill

## When to Use
- Profile CSV datasets
- Generate statistics and summary for data exploration

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| csv | path | Yes | Path to the CSV file to profile |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| profile.md | markdown | Human-readable profile report |
| profile.json | json | Machine-readable profile data |

## Guardrails

### Allowed
- Read CSV files and compute statistics
- Generate markdown reports
- Profile column data types and distributions

### Forbidden
- Modify or write to input files
- Upload data externally
- Execute arbitrary code from data

## Example
```bash
skillpack profile-dataset --csv data.csv
```

## Related Skills
- data-quality - Generate validation schemas from profiled data
- dbt-generator - Generate dbt models from schema
