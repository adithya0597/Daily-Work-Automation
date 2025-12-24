# Git Workflow Skill

## When to Use
- Create feature branches, format commits, and generate PR templates.
- Automate git workflow generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| type | string | No | Branch type |
| description | string | No | Brief description (will be slugified) |
| issue | string | No | Issue/ticket number (e.g., JIRA-123) |
| type | string | No | Commit type |
| scope | string | No | Scope of the change |
| description | string | No | Commit description |
| breaking | string | No | Mark as breaking change |
| title | string | No | PR title |
| branch | string | No | Branch name (defaults to current) |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| PR_TEMPLATE.md | file | Generated output |

## Example
```bash
skillpack git-workflow --name example
```

## Related Skills
- Check skillpack --help for related skills
