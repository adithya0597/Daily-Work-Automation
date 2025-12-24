# Daily Ops Summary Skill

## When to Use
- Generate daily operations status reports
- Create Slack-ready summaries

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| date | string | No | Date (YYYY-MM-DD), defaults to today |
| metrics | path | No | Path to metrics YAML file |
| team | string | No | Team name (default: Data Platform) |
| output-dir | path | No | Output directory |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| ops_summary_{date}.md | markdown | Full operations summary |
| slack_message_{date}.txt | text | Slack-formatted message |
| metrics_{date}.yaml | yaml | Metrics snapshot |

## Example
```bash
skillpack daily-ops-summary --date 2024-01-15 --team "Data Platform"
```

## Related Skills
- pipeline-doctor - Diagnose pipeline issues
- backfill-planner - Plan backfills
