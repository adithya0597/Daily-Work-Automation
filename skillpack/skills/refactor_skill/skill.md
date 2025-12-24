# Refactor Skill Skill

## When to Use
- Identify complexity hotspots and propose safe refactors.
- Automate refactor skill generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| source | string | No | Path to Python source file or directory |
| threshold | string | No | Complexity threshold for flagging (default: 10) |
| output-dir | string | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| refactor_report.md | file | Generated output |
| metrics.json | file | Generated output |

## Example
```bash
skillpack refactor-skill --name example
```

## Related Skills
- Check skillpack --help for related skills
