# Project Scaffolding Skill

## When to Use
- Starting a new Python project
- Need consistent project structure
- Want pre-configured CI, linting, type checking

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Project name |
| description | string | No | Project description |

## Outputs
Complete project structure in `./out/project_scaffolding/{name}/`

## Procedure
1. **Validate name** - Must be valid Python identifier
2. **Create directories** - src/, tests/, .github/, .vscode/
3. **Generate files** - pyproject.toml, README, etc.
4. **Write outputs** - All files to output directory

## Guardrails
### Allowed
- Create files in ./out/project_scaffolding/
- Read internal templates

### Forbidden
- Overwrite existing projects
- Modify files outside ./out/

## Example
```bash
skillpack project-scaffolding --name my-app --description "My application"
```
