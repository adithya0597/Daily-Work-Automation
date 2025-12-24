# Experiment Tracking Skill

## When to Use
- Generate MLflow or W&B tracking boilerplate.
- Automate experiment tracking generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | No | Project name |
| tracker | string | No | Tracking framework |
| output-dir | string | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| mlflow_tracker.py | file | Generated output |
| wandb_tracker.py | file | Generated output |
| tracker.py | file | Generated output |
| tracking_config.yaml | file | Generated output |

## Example
```bash
skillpack experiment-tracking --name example
```

## Related Skills
- Check skillpack --help for related skills
