# Dag Authoring Skill

## When to Use
- Generate DAG code for Airflow, Prefect, or Dagster
- Create pipeline orchestration from templates

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | DAG/Flow name |
| framework | string | No | Target: airflow, prefect, or dagster (default: airflow) |
| schedule | string | No | Schedule expression, e.g., @daily |
| config | path | No | Pipeline config YAML file |
| output-dir | path | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| {name}_dag.py | python | Generated DAG/flow code |
| {name}_runbook.md | markdown | Deployment runbook |

## Example
```bash
skillpack dag-authoring --name my_pipeline --framework airflow --schedule "@daily"
```

## Related Skills
- backfill-planner - Generate backfill plans for DAGs
- pipeline-doctor - Diagnose pipeline issues
