# Project Scaffolding Skill

## When to Use
- Starting a new Python project
- Need consistent project structure
- Want pre-configured CI, linting, type checking

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | Yes | Project name (alphanumeric and hyphens) |
| description | string | No | Project description |

## Outputs
Complete project structure in `./out/project_scaffolding/{name}/`:
- pyproject.toml, README.md, .gitignore
- src/, tests/, .github/, .vscode/

## Procedure
1. **Validate name** - Must be valid Python identifier
2. **Create directories** - src/, tests/, .github/, .vscode/
3. **Generate files** - Apply templates with name/description
4. **Write outputs** - All files to output directory

## Guardrails

### Allowed
- Create files in ./out/project_scaffolding/
- Read internal templates

### Forbidden
- Overwrite existing projects without confirmation
- Modify files outside ./out/
- Execute generated code

## Preconditions
- [ ] Project name is valid identifier
- [ ] Output directory is writable

## Postconditions
- [ ] All project files created
- [ ] No existing files modified

## Error Handling
| Error | Condition | Recovery |
|-------|-----------|----------|
| InvalidName | Name has invalid characters | Use alphanumeric + hyphens only |
| DirectoryExists | Project already exists | Choose different name |

## Examples
```bash
skillpack project-scaffolding --name my-app
skillpack project-scaffolding --name data-pipeline --description "ETL for sales"
```

## Related Skills
- **quality-gate**: Run quality checks on generated project
- **pr-summary**: Generate PR summary for initial commit
