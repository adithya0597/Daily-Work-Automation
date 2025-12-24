# Git Workflow Skill

## When to Use
- Starting new work (create feature branch)
- Committing changes (format conventional commit)
- Creating pull requests (generate PR template)

## Actions

### branch
Creates a properly named feature branch.

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| --type | enum | No | feature, bugfix, hotfix, release, chore |
| --description | string | Yes | Brief description (slugified) |
| --issue | string | No | Issue/ticket number |

### commit
Formats a conventional commit message.

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| --type | enum | No | feat, fix, docs, style, refactor, test, chore |
| --scope | string | No | Scope of change |
| --description | string | Yes | Commit description |
| --breaking | flag | No | Mark as breaking change |

### pr
Generates a PR template.

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| --title | string | Yes | PR title |
| --branch | string | No | Branch name (defaults to current) |

## Outputs
- Branch: Command to run
- Commit: Command to run
- PR: `./out/git_workflow/PR_TEMPLATE.md`

## Procedure
1. **Parse action** - Determine branch/commit/pr
2. **Validate inputs** - Check required fields
3. **Generate output** - Create command or file
4. **Return result** - Show command to run

## Guardrails

### Allowed
- Generate branch names
- Format commit messages
- Create PR templates in ./out/

### Forbidden
- Execute git commands directly
- Modify repository state
- Access git credentials

## Preconditions
- [ ] Git repository exists

## Postconditions
- [ ] Output is valid for the action type

## Error Handling
| Error | Condition | Recovery |
|-------|-----------|----------|
| InvalidAction | Unknown action | Use branch/commit/pr |
| MissingDescription | No description | Provide --description |

## Examples

### Create Feature Branch
```bash
skillpack git-workflow branch --type feature --description "add user auth"
# Output: git checkout -b feature/add-user-auth
```

### With Issue Number
```bash
skillpack git-workflow branch --description "login page" --issue PROJ-123
# Output: git checkout -b feature/PROJ-123-login-page
```

### Format Commit
```bash
skillpack git-workflow commit --type feat --scope auth --description "add login"
# Output: git commit -m "feat(auth): add login"
```

### Breaking Change
```bash
skillpack git-workflow commit --type feat --description "new API" --breaking
# Output: git commit -m "feat!: new API"
```

### Generate PR Template
```bash
skillpack git-workflow pr --title "Add User Authentication"
# Creates ./out/git_workflow/PR_TEMPLATE.md
```

## Related Skills
- **pr-summary**: Generate change summary for PRs
- **quality-gate**: Run before committing
