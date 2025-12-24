# Baseline Model Factory Skill

## When to Use
- Build scikit-learn baselines with proper pipelines and config.
- Automate baseline model factory generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | No | Model name |
| task | string | No | ML task type |
| config | string | No | Path to model configuration YAML |
| output-dir | string | No | Output directory |
| data | string | No | Path to training data CSV |
| output | string | No | Output directory |
| model | string | No | Model to save as primary |
| model | string | No | Path to saved model |
| data | string | No | Path to evaluation data |
| target | string | No | Target column name |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| train.py | file | Generated output |
| config.yaml | file | Generated output |
| evaluate.py | file | Generated output |
| README.md | file | Generated output |

## Example
```bash
skillpack baseline-model-factory --name example
```

## Related Skills
- Check skillpack --help for related skills
