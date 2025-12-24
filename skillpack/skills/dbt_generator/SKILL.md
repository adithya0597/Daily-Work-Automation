# Dbt Generator Skill

## When to Use
- Generate dbt models and tests.
- Automate dbt generator generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| config | string | No | Path to config file (YAML or JSON). If not provided, generates an example. |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| output.md | file | Generated output |

## Example
```bash
skillpack dbt-generator --name example
```

## Related Skills
- Check skillpack --help for related skills
