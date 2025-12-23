# PR Summary Skill

## When to Use
- Before creating a pull request
- To assess change risk
- To generate rollback plans

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| diff_file | file_path | Yes | Path to unified diff file |
| title | string | No | PR title (default: "Pull Request Summary") |

## Outputs
`./out/pr_summary/PR_SUMMARY.md` containing:
- Overview (files changed, lines added/removed)
- Risk Assessment (LOW/MEDIUM/HIGH)
- Files Changed list
- Rollout/Rollback plans
- Testing checklist

## Procedure
1. **Parse diff** - Extract files and line counts
2. **Assess risk** - Based on size, file types, sensitive files
3. **Generate summary** - Create markdown report
4. **Write output** - Save to ./out/

## Guardrails

### Allowed
- Read specified diff file
- Parse unified diff format
- Write to ./out/pr_summary/
- Calculate statistics

### Forbidden
- Execute git commands
- Modify repository files
- Access git history or refs
- Delete any files

## Preconditions
- [ ] Diff file exists and is readable
- [ ] Diff is in unified format

## Postconditions
- [ ] PR_SUMMARY.md created
- [ ] All sections populated
- [ ] Input file unchanged

## Error Handling
| Error | Condition | Recovery |
|-------|-----------|----------|
| FileNotFoundError | Diff file missing | Check path |
| InvalidDiffFormat | Not unified diff | Use git diff output |
| EmptyDiff | No changes | Provide diff with changes |

## Risk Assessment Factors
- Large changes (>500 lines): +2 risk
- Many files (>20): +2 risk
- Database changes (.sql, migrations): +1 risk
- Config changes (.yml, .env): +1 risk

## Examples
```bash
git diff main..HEAD > changes.diff
skillpack pr-summary --diff-file changes.diff
skillpack pr-summary --diff-file changes.diff --title "Feature: Auth"
```

## Related Skills
- **quality-gate**: Run quality checks before PR
- **schema-diff**: Analyze database changes
