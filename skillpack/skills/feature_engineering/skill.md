# Feature Engineering Skill

## When to Use
- Suggest and generate feature transformations per column type.
- Automate feature engineering generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| config | string | No | Path to column configuration YAML |
| output-dir | string | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| features.py | file | Generated output |
| transformations.md | file | Generated output |
| feature_config.yaml | file | Generated output |

## Example
```bash
skillpack feature-engineering --name example
```

## Related Skills
- Check skillpack --help for related skills
