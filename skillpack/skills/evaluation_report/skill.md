# Evaluation Report Skill

## When to Use
- Generate model evaluation reports with metrics and plots.
- Automate evaluation report generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | No | Model name |
| task | string | No | Task type |
| metrics | string | No | Path to metrics YAML file |
| output-dir | string | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| evaluation_report.md | file | Generated output |
| evaluate.py | file | Generated output |
| plot_results.py | file | Generated output |
| metrics.yaml | file | Generated output |

## Example
```bash
skillpack evaluation-report --name example
```

## Related Skills
- Check skillpack --help for related skills
