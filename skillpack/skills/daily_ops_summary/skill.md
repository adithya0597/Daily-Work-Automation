# Daily Ops Summary Skill

## When to Use
- Generate daily status report from pipeline and system health.
- Automate daily ops summary generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| date | string | No | Date for summary (YYYY-MM-DD) |
| metrics | string | No | Path to metrics YAML file |
| team | string | No | Team name for the report |
| output-dir | string | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| output.md | file | Generated output |

## Example
```bash
skillpack daily-ops-summary --name example
```

## Related Skills
- Check skillpack --help for related skills
