# PR Summary Skill

## When to Use
- Analyze PR diffs for changes and risk
- Generate rollout/rollback plans

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| diff-file | path | Yes | Path to the diff file to analyze |
| title | string | No | Title for the summary |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| PR_SUMMARY.md | markdown | Summary with risk assessment, rollout plan |

## Example
```bash
# Generate diff first
git diff main..feature-branch > changes.diff

# Generate summary
skillpack pr-summary --diff-file changes.diff --title "Feature X"
```

## Related Skills
- git-workflow - Generate commit messages and templates
