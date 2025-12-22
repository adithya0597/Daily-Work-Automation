---
name: pr_summary
description: Generate PR summaries with risk assessment from git diffs
tags: [pr, git, review, risk]
activation_triggers:
  - "summarize PR"
  - "analyze diff"
  - "review changes"
version: "0.1.0"
dependencies: []
---

# PR Summary Skill

## Overview

Analyzes git diffs and generates comprehensive PR summaries including:
- Change statistics (files, lines added/removed)
- Risk assessment with specific risk factors
- File type breakdown
- Rollout and rollback plans
- Testing checklist

## Workflow

1. Parse unified diff format to extract file changes
2. Analyze changes for risk factors
3. Generate markdown summary with all sections
4. Write to `./out/pr_summary/PR_SUMMARY.md`

## Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--diff-file` | Yes | - | Path to diff file |
| `--title` | No | "Pull Request Summary" | Title for the summary |

## Outputs

```
./out/pr_summary/
└── PR_SUMMARY.md
```

The summary includes:
- Overview (files, lines changed)
- Risk Assessment (LOW/MEDIUM/HIGH)
- Risk Factors list
- File Types Changed
- Files Changed list
- Rollout Plan
- Rollback Plan
- Testing Checklist

## Error Handling

- File not found: Returns error with clear message
- Empty diff: Generates summary with zero changes

## Examples

```bash
# Generate diff and summarize
git diff main..feature > changes.diff
skillpack pr-summary --diff-file changes.diff

# With custom title
skillpack pr-summary --diff-file changes.diff --title "Feature: User Authentication"
```

## Related Skills

- `quality-gate`: Run quality checks before creating PR
- `schema-diff`: Analyze database schema changes in the PR
