# Pr Summary Skill

## When to Use
- Generate PR summaries with risk assessment from diffs.
- Automate pr summary generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| diff-file | string | No | Path to the diff file to analyze |
| title | string | No | Title for the summary (default:  |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| output.md | file | Generated output |

## Example
```bash
skillpack pr-summary --name example
```

## Related Skills
- Check skillpack --help for related skills
