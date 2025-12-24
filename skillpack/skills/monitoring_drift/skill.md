# Monitoring Drift Skill

## When to Use
- Generate data and prediction drift detection templates.
- Automate monitoring drift generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | No | Model/dataset name |
| type | string | No | Type of drift to monitor |
| output-dir | string | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| data_drift.py | file | Generated output |
| prediction_drift.py | file | Generated output |
| alerting.yaml | file | Generated output |
| dashboard.json | file | Generated output |
| README.md | file | Generated output |

## Example
```bash
skillpack monitoring-drift --name example
```

## Related Skills
- Check skillpack --help for related skills
