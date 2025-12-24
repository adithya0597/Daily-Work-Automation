# Containerization Skill

## When to Use
- Generate Dockerfile and compose configs for services.
- Automate containerization generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | No | Service name |
| base | string | No | Base image type |
| runtime | string | No | Runtime type |
| port | string | No | Exposed port |
| compose | string | No | Generate docker-compose.yml |
| output-dir | string | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| Dockerfile | file | Generated output |
| .dockerignore | file | Generated output |
| docker-compose.yml | file | Generated output |
| Makefile | file | Generated output |
| DOCKER_README.md | file | Generated output |

## Example
```bash
skillpack containerization --name example
```

## Related Skills
- Check skillpack --help for related skills
