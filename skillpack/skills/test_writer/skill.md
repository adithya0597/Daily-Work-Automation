# Test Writer Skill

## When to Use
- Generate pytest tests from code.
- Automate test writer generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| source | string | No | Path to Python source file |
| output-dir | string | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| conftest.py | file | Generated output |

## Example
```bash
skillpack test-writer --name example
```

## Related Skills
- Check skillpack --help for related skills
