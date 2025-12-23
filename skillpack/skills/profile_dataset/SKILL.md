# Profile Dataset Skill

## When to Use
- Before loading data to a database to understand structure
- When validating data quality before processing
- To identify null values, outliers, and data types
- When exploring a new dataset for the first time

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| csv_path | file_path | Yes | Path to the CSV file to profile |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| profile.md | Markdown | Human-readable profile report |
| profile.json | JSON | Machine-readable profile data |

Output directory: `./out/profile_dataset/`

## Procedure
1. **Validate Input** - Check file exists and is readable
2. **Load Dataset** - Read CSV with headers, count rows/columns
3. **Infer Column Types** - Parse as integer → float → boolean → string
4. **Calculate Statistics** - Null counts, unique values, numeric stats
5. **Generate Reports** - Write profile.md and profile.json

## Guardrails

### Allowed
- Read the specified CSV file
- Parse CSV content with headers
- Calculate statistics (count, mean, min, max, etc.)
- Write to ./out/profile_dataset/

### Forbidden
- Modify the input CSV file
- Delete any files
- Execute arbitrary code
- Access files other than the specified CSV
- Make network requests

## Example
```bash
skillpack profile-dataset --csv data/users.csv
```
