# Iac Boilerplate Skill

## When to Use
- Generate Terraform modules for cloud infrastructure.
- Automate iac boilerplate generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | No | Project name |
| cloud | string | No | Cloud provider |
| resources | string | No | Comma-separated resources to generate |
| output-dir | string | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| main.tf | file | Generated output |
| variables.tf | file | Generated output |
| outputs.tf | file | Generated output |
| main.tf | file | Generated output |
| terraform.tfvars.example | file | Generated output |

## Example
```bash
skillpack iac-boilerplate --name example
```

## Related Skills
- Check skillpack --help for related skills
