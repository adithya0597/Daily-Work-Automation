# Cost Regression Skill

## When to Use
- Detect cost and performance regression in infrastructure.
- Automate cost regression generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | No | Project name |
| metrics | string | No | Path to metrics YAML file |
| threshold | string | No | Regression threshold (default: 10%) |
| output-dir | string | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| cost_analyzer.py | file | Generated output |
| perf_analyzer.py | file | Generated output |
| check_regression.py | file | Generated output |
| cost-check.yml | file | Generated output |
| regression_report.md | file | Generated output |

## Example
```bash
skillpack cost-regression --name example
```

## Related Skills
- Check skillpack --help for related skills
