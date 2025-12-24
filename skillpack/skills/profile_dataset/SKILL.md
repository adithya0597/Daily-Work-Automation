# Profile Dataset Skill

## When to Use
- Profile CSV datasets
- Generate statistics and summary for data exploration
- Automate profile dataset generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| csv | file_path | Yes | Path to the CSV file to profile |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| profile-report.md | markdown | Statistical profile of the dataset |

## Guardrails

### Allowed
- Read CSV files and compute statistics
- Generate markdown reports
- Profile column data types and distributions

### Forbidden
- Modify or write to input files
- Upload data externally
- Execute arbitrary code from data

## Preconditions
- [ ] Input CSV file exists
- [ ] File is readable

## Postconditions
- [ ] Profile report created in output directory

## Example
```bash
skillpack profile-dataset --csv data.csv
```

## Related Skills
- data-quality - Generate validation schemas from profiled data
- dbt-generator - Generate dbt models from schema
