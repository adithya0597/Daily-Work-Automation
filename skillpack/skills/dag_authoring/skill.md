# Dag Authoring Skill

## When to Use
- Generate DAG code for Airflow, Prefect, or Dagster.
- Automate dag authoring generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | No | DAG/Flow name |
| framework | string | No | Target orchestration framework |
| config | string | No | Path to pipeline configuration YAML |
| schedule | string | No | Schedule expression (e.g., @daily, 0 0 * * *) |
| output-dir | string | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| output.md | file | Generated output |

## Example
```bash
skillpack dag-authoring --name example
```

## Related Skills
- Check skillpack --help for related skills
