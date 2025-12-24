# Pipeline Doctor Skill

## When to Use
- Diagnose pipeline issues from logs and configs.
- Automate pipeline doctor generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| logs | string | No | Path to log file or directory |
| config | string | No | Path to pipeline config (optional) |
| output-dir | string | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| diagnosis.md | file | Generated output |
| remediation.md | file | Generated output |

## Example
```bash
skillpack pipeline-doctor --name example
```

## Related Skills
- Check skillpack --help for related skills
