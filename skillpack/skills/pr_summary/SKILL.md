# PR Summary Skill

## When to Use
- Before creating a pull request
- To assess change risk
- To generate rollback plans

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| diff_file | file_path | Yes | Path to unified diff file |
| title | string | No | PR title |

## Outputs
`./out/pr_summary/PR_SUMMARY.md` containing:
- Overview (files changed, lines)
- Risk Assessment (LOW/MEDIUM/HIGH)
- Files Changed list
- Rollout/Rollback plans

## Procedure
1. **Parse diff** - Extract files and line counts
2. **Assess risk** - Based on size, file types
3. **Generate summary** - Create markdown report
4. **Write output** - Save to ./out/

## Guardrails
### Allowed
- Read specified diff file
- Write to ./out/pr_summary/

### Forbidden
- Execute git commands
- Modify repository files

## Example
```bash
git diff main..HEAD > changes.diff
skillpack pr-summary --diff-file changes.diff
```
