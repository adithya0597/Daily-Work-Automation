---
name: profile_dataset
description: Profile CSV datasets with statistics and data quality insights
tags: [data, csv, profiling, analysis]
activation_triggers:
  - "profile data"
  - "analyze csv"
  - "data statistics"
version: "0.1.0"
dependencies: []
---

# Profile Dataset Skill

## Overview

Profiles CSV files to generate comprehensive statistics:
- Row and column counts
- Data types per column
- Null/missing value counts
- Unique value counts
- Numeric statistics (min, max, mean, median, std dev)
- String length statistics

## Workflow

1. Read CSV file with header detection
2. Infer data types for each column
3. Calculate statistics per column
4. Generate JSON and Markdown outputs
5. Write to `./out/profile_dataset/`

## Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--csv` | Yes | - | Path to CSV file |

## Outputs

```
./out/profile_dataset/
├── profile.json    # Machine-readable profile
└── profile.md      # Human-readable report
```

## Error Handling

- File not found: Returns error with path
- No headers: Returns error
- Encoding issues: Tries UTF-8

## Examples

```bash
# Profile a CSV file
skillpack profile-dataset --csv data/users.csv

# View the generated report
cat ./out/profile_dataset/profile.md
```

## Related Skills

- `data-quality`: Generate validation schemas based on profile
- `schema-diff`: Compare schema changes over time
