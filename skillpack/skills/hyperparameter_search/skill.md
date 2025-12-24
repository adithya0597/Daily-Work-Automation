# Hyperparameter Search Skill

## When to Use
- Generate Optuna or Ray Tune sweep templates.
- Automate hyperparameter search generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | No | Experiment name |
| framework | string | No | HPO framework |
| model | string | No | Model type |
| output-dir | string | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| optuna_sweep.py | file | Generated output |
| ray_tune_sweep.py | file | Generated output |
| wandb_sweep.py | file | Generated output |
| sweep_config.yaml | file | Generated output |
| search_space.yaml | file | Generated output |

## Example
```bash
skillpack hyperparameter-search --name example
```

## Related Skills
- Check skillpack --help for related skills
