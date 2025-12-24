# Fastapi Serving Skill

## When to Use
- Wrap models in FastAPI services with validation and health endpoints.
- Automate fastapi serving generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | No | Model/service name |
| type | string | No | Model type |
| output-dir | string | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| main.py | file | Generated output |
| schemas.py | file | Generated output |
| Dockerfile | file | Generated output |
| requirements.txt | file | Generated output |
| test_api.py | file | Generated output |

## Example
```bash
skillpack fastapi-serving --name example
```

## Related Skills
- Check skillpack --help for related skills
