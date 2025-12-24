# Notebook To Package Skill

## When to Use
- Convert Jupyter notebooks to Python packages.
- Automate notebook to package generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| notebook | string | No | Path to Jupyter notebook (.ipynb) |
| name | string | No | Package name (defaults to notebook name) |
| output-dir | string | No | Output directory |
| input | string | No | Input file path |
| output | string | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| pyproject.toml | file | Generated output |
| README.md | file | Generated output |

## Example
```bash
skillpack notebook-to-package --name example
```

## Related Skills
- Check skillpack --help for related skills
