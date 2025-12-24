# Experiment Queue Skill

## When to Use
- Manage experiment queue with checkpointing.
- Automate experiment queue generation

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | No | Queue name |
| output-dir | string | No | Output directory |
| config | string | No | Resume from checkpoint |
| status | string | No | Show queue status |

## Outputs
| File | Format | Description |
|------|--------|-------------|
| queue_manager.py | file | Generated output |
| run_queue.py | file | Generated output |
| experiments.yaml | file | Generated output |
| checkpoint.json | file | Generated output |

## Example
```bash
skillpack experiment-queue --name example
```

## Related Skills
- Check skillpack --help for related skills
