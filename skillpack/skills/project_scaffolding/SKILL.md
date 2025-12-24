# Project Scaffolding Skill

## When to Use
- Create a new Python project from template
- Generate project structure with CI, tests, etc.

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Name of the project to create |
| description | string | No | Project description |

## Outputs
Creates a project directory with:
- `pyproject.toml` - Project configuration
- `README.md` - Documentation
- `src/{name}/` - Source package
- `tests/` - Test directory
- `.github/workflows/ci.yml` - CI configuration
- `.gitignore` - Git ignore file

## Example
```bash
skillpack project-scaffolding --name my_project --description "My new project"
```

## Related Skills
- quality-gate - Run quality checks on new projects
