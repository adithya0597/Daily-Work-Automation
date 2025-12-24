# Backfill Planner Skill

## When to Use
- Generate backfill plans with date ranges and checkpoints.
- Automate backfill planner generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | No | Pipeline name |
| start-date | string | No | Start date (YYYY-MM-DD) |
| end-date | string | No | End date (YYYY-MM-DD) |
| partition-by | string | No | Partition granularity |
| batch-size | string | No | Batch size for parallel runs |
| output-dir | string | No | Output directory |
| batch | string | No | Run specific batch |
| partition | string | No | Run specific partition |
| resume | string | No | Resume from checkpoint |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| backfill_plan.md | file | Generated output |
| backfill.py | file | Generated output |
| checkpoint.json | file | Generated output |

## Example
```bash
skillpack backfill-planner --name example
```

## Related Skills
- Check skillpack --help for related skills
