# Skillpack

**Production-grade engineering skills for daily work automation.**

Skillpack is a CLI toolkit that provides deterministic, auditable, and runnable engineering skills for data engineering, software development, and DevOps workflows.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Skills Reference](#skills-reference)
  - [Project Scaffolding](#1-project-scaffolding)
  - [Quality Gate](#2-quality-gate)
  - [PR Summary](#3-pr-summary)
  - [Profile Dataset](#4-profile-dataset)
  - [Data Quality](#5-data-quality)
  - [SQL Refiner](#6-sql-refiner)
  - [Schema Diff](#7-schema-diff)
  - [dbt Generator](#8-dbt-generator)
- [Real-World Testing Guide](#real-world-testing-guide)
- [Output Convention](#output-convention)
- [Development](#development)
- [License](#license)

---

## Features

| Feature | Description |
|---------|-------------|
| **Deterministic** | Same inputs → same outputs, with stable ordering |
| **Auditable** | Never silently mutates or deletes existing files |
| **Safe** | No destructive shell ops, no remote writes, no deployments |
| **Runnable** | Single CLI: `skillpack <skill> [args...]` |
| **Tested** | Every skill has smoke tests + CI pipeline |

---

## Installation

### From Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/skillpack.git
cd skillpack

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Verify installation
skillpack --version
skillpack --help
```

### Dependencies

- Python 3.11+
- pandas (data processing)
- pandera (data validation)
- PyYAML (configuration)

---

## Quick Start

```bash
# See all available skills
skillpack --help

# Generate a new Python project
skillpack project-scaffolding --name my-awesome-app

# Profile a CSV dataset
skillpack profile-dataset --csv data/users.csv

# Generate a PR summary from a git diff
git diff main..feature > changes.diff
skillpack pr-summary --diff-file changes.diff

# Run quality checks
skillpack quality-gate
```

---

## Skills Reference

### 1. Project Scaffolding

Generate a complete Python project skeleton with modern best practices.

**Command:**
```bash
skillpack project-scaffolding --name <project-name> [--description "Your description"]
```

**Example:**
```bash
skillpack project-scaffolding --name data-pipeline --description "ETL pipeline for customer data"
```

**Output:**
```
./out/project_scaffolding/data-pipeline/
├── pyproject.toml          # Modern Python packaging
├── README.md               # Project documentation
├── .gitignore              # Python-specific ignores
├── .env.example            # Environment template
├── .pre-commit-config.yaml # Pre-commit hooks
├── .github/workflows/ci.yml # GitHub Actions CI
├── .vscode/settings.json   # VS Code configuration
├── src/
│   ├── __init__.py
│   └── main.py
└── tests/
    ├── __init__.py
    └── test_main.py
```

**Real-World Use:**
```bash
# Create a new microservice
skillpack project-scaffolding --name auth-service --description "Authentication microservice"
cp -r out/project_scaffolding/auth-service ~/projects/
cd ~/projects/auth-service
pip install -e ".[dev]"
pytest tests/
```

---

### 2. Quality Gate

Run comprehensive quality checks: format, lint, type-check, and tests.

**Command:**
```bash
skillpack quality-gate [--check]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--check` | Check-only mode (no file modifications) |

**What It Runs:**
1. `ruff format` - Code formatting
2. `ruff check --fix` - Linting with auto-fix
3. `mypy` - Type checking
4. `pytest` - Unit tests

**Example:**
```bash
# Fix issues and run tests
skillpack quality-gate

# CI mode: check only, fail on issues
skillpack quality-gate --check
```

**Real-World Use:**
```bash
# Add to your project's Makefile
echo 'quality:
	skillpack quality-gate' >> Makefile

# Run before every commit
make quality
```

---

### 3. PR Summary

Generate a comprehensive PR summary with risk assessment from git diffs.

**Command:**
```bash
skillpack pr-summary --diff-file <path> [--title "PR Title"]
```

**Example:**
```bash
# Generate diff from your current branch
git diff main..HEAD > my-changes.diff

# Generate summary
skillpack pr-summary --diff-file my-changes.diff --title "Feature: User Authentication"
```

**Output (`./out/pr_summary/PR_SUMMARY.md`):**
- Overview (files changed, lines added/removed)
- Risk Assessment (LOW/MEDIUM/HIGH)
- Risk Factors (large changes, sensitive files, etc.)
- Files Changed list
- Rollout Plan
- Rollback Plan
- Testing Checklist

**Real-World Use:**
```bash
# Integrate with git workflow
git diff origin/main...HEAD > /tmp/pr.diff
skillpack pr-summary --diff-file /tmp/pr.diff --title "$(git log -1 --pretty=%B)"
cat out/pr_summary/PR_SUMMARY.md
```

---

### 4. Profile Dataset

Profile CSV datasets with comprehensive statistics.

**Command:**
```bash
skillpack profile-dataset --csv <path-to-csv>
```

**Example:**
```bash
skillpack profile-dataset --csv data/customers.csv
```

**Output:**
```
./out/profile_dataset/
├── profile.md      # Human-readable report
└── profile.json    # Machine-readable data
```

**Statistics Generated:**
- Row/column counts, file size
- Per-column: type, null count, unique values
- Numeric columns: min, max, mean, median, std dev
- String columns: min/max/avg length
- Sample values

**Real-World Use:**
```bash
# Profile before loading to database
skillpack profile-dataset --csv raw_data/sales_2024.csv

# Check for data quality issues
cat out/profile_dataset/profile.md | grep -E "(Null|null)"

# Use JSON output in pipelines
cat out/profile_dataset/profile.json | jq '.columns[] | select(.null_count > 0)'
```

---

### 5. Data Quality

Generate Pandera validation schemas for DataFrame validation.

**Command:**
```bash
skillpack data-quality [--config <path>]
```

**Example with Config:**
```bash
# Create a schema config file
cat > schema_config.yaml << 'EOF'
name: OrderSchema
columns:
  - name: order_id
    type: integer
    nullable: false
    unique: true
    checks:
      - type: min
        value: 1
  - name: customer_email
    type: string
    nullable: false
    checks:
      - type: regex
        pattern: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
  - name: amount
    type: float
    nullable: false
    checks:
      - type: between
        min: 0.01
        max: 100000
  - name: status
    type: string
    nullable: false
    checks:
      - type: isin
        values: ["pending", "completed", "cancelled"]
EOF

skillpack data-quality --config schema_config.yaml
```

**Output:**
```
./out/data_quality/
├── schema.py           # Pandera schema definition
└── run_validation.py   # Validation runner script
```

**Real-World Use:**
```bash
# Generate schema
skillpack data-quality --config my_schema.yaml

# Copy to your project
cp out/data_quality/schema.py my_project/validation/

# Validate data in your pipeline
python out/data_quality/run_validation.py data/orders.csv
```

---

### 6. SQL Refiner

Generate SQL queries from natural language questions.

**Command:**
```bash
skillpack sql-refiner --question "<question>" [--dialect postgres|bigquery|snowflake]
```

**Examples:**
```bash
# PostgreSQL (default)
skillpack sql-refiner --question "How many active users signed up in the last 30 days"

# BigQuery
skillpack sql-refiner --question "Get top 10 orders by amount" --dialect bigquery

# Snowflake
skillpack sql-refiner --question "Calculate average order value per customer" --dialect snowflake
```

**Output:**
```
./out/sql_refiner/
├── query.sql        # Generated SQL query
├── explain.sql      # EXPLAIN query for performance
└── query_notes.md   # Usage notes and placeholders
```

**Real-World Use:**
```bash
# Generate a query template
skillpack sql-refiner \
  --question "Find customers who haven't ordered in 90 days" \
  --dialect postgres

# Review and customize
cat out/sql_refiner/query.sql

# Copy to your queries
cp out/sql_refiner/query.sql analytics/queries/inactive_customers.sql
```

---

### 7. Schema Diff

Compare database schemas and generate migration scripts.

**Command:**
```bash
skillpack schema-diff --old <old-schema.json> --new <new-schema.json> [--table <table-name>]
```

**Schema JSON Format:**
```json
{
  "columns": [
    {"name": "id", "type": "INTEGER", "nullable": false, "pk": true},
    {"name": "email", "type": "VARCHAR(255)", "nullable": false},
    {"name": "created_at", "type": "TIMESTAMP", "nullable": true}
  ]
}
```

**Example:**
```bash
# Create old schema
echo '{"columns": [
  {"name": "id", "type": "INTEGER", "nullable": false, "pk": true},
  {"name": "name", "type": "VARCHAR(100)", "nullable": true}
]}' > old_schema.json

# Create new schema with changes
echo '{"columns": [
  {"name": "id", "type": "INTEGER", "nullable": false, "pk": true},
  {"name": "name", "type": "VARCHAR(100)", "nullable": false},
  {"name": "email", "type": "VARCHAR(255)", "nullable": true}
]}' > new_schema.json

# Generate migration
skillpack schema-diff --old old_schema.json --new new_schema.json --table users
```

**Output:**
```
./out/schema_diff/
├── migration.sql   # Forward + rollback SQL
└── migration.md    # Impact documentation
```

**Real-World Use:**
```bash
# Export current schema from PostgreSQL
psql -c "\\d+ users" > current_schema.txt
# (Convert to JSON format manually or with a script)

# Compare with proposed changes
skillpack schema-diff --old current.json --new proposed.json --table users

# Review migration
cat out/schema_diff/migration.sql
cat out/schema_diff/migration.md
```

---

### 8. dbt Generator

Generate dbt models, tests, and documentation from configuration.

**Command:**
```bash
skillpack dbt-generator [--config <path>]
```

**Example Config (`dbt_config.yaml`):**
```yaml
project_name: E-Commerce Analytics
description: dbt project for e-commerce data analytics

sources:
  - source_name: raw
    table_name: orders
    columns:
      - name: id
        alias: order_id
        tests: [unique, not_null]
      - name: user_id
        tests: [not_null]
      - name: amount
      - name: created_at

models:
  - name: mart_daily_revenue
    description: Daily revenue aggregation
    refs:
      - name: stg_orders
        alias: orders
    columns:
      - name: order_date
        source: orders
    aggregations:
      - function: SUM
        column: orders.amount
        alias: total_revenue
      - function: COUNT
        column: orders.order_id
        alias: order_count
    group_by:
      - orders.order_date
```

**Example:**
```bash
skillpack dbt-generator --config dbt_config.yaml
```

**Output:**
```
./out/dbt_generator/
└── models/
    ├── staging/
    │   └── stg_orders.sql
    ├── marts/
    │   └── mart_daily_revenue.sql
    ├── schema.yml
    └── docs.md
```

**Real-World Use:**
```bash
# Generate dbt models
skillpack dbt-generator --config dbt_config.yaml

# Copy to your dbt project
cp -r out/dbt_generator/models/* my_dbt_project/models/

# Run dbt
cd my_dbt_project
dbt run
dbt test
```

---

## Real-World Testing Guide

### Scenario 1: New Project Setup

```bash
# 1. Create project structure
skillpack project-scaffolding --name my-data-pipeline \
  --description "ETL pipeline for sales data"

# 2. Move to workspace
mv out/project_scaffolding/my-data-pipeline ~/projects/

# 3. Initialize and test
cd ~/projects/my-data-pipeline
pip install -e ".[dev]"
pytest tests/  # Should pass

# 4. Run quality checks
skillpack quality-gate
```

### Scenario 2: Data Pipeline Development

```bash
# 1. Profile incoming data
skillpack profile-dataset --csv raw_data/sales.csv
# Review: out/profile_dataset/profile.md

# 2. Create validation schema based on profile
cat > sales_schema.yaml << 'EOF'
name: SalesSchema
columns:
  - name: sale_id
    type: integer
    nullable: false
    unique: true
  - name: amount
    type: float
    nullable: false
    checks:
      - type: min
        value: 0
EOF
skillpack data-quality --config sales_schema.yaml

# 3. Generate dbt models
skillpack dbt-generator --config dbt_config.yaml
```

### Scenario 3: PR Review Workflow

```bash
# Before submitting PR:

# 1. Run quality checks
skillpack quality-gate

# 2. Generate PR summary
git diff main..HEAD > changes.diff
skillpack pr-summary --diff-file changes.diff \
  --title "Add user authentication feature"

# 3. Review generated summary
cat out/pr_summary/PR_SUMMARY.md

# 4. Include in PR description or attach as comment
```

### Scenario 4: Database Migration

```bash
# 1. Document current schema
# (Export from your database)

# 2. Create new schema JSON
# (After planning changes)

# 3. Generate migration
skillpack schema-diff \
  --old schemas/users_v1.json \
  --new schemas/users_v2.json \
  --table users

# 4. Review before applying
cat out/schema_diff/migration.sql
cat out/schema_diff/migration.md

# 5. Apply migration (manually or via your migration tool)
```

---

## Output Convention

All skill outputs go to `./out/<skill_name>/`:

```
./out/
├── project_scaffolding/<project_name>/
├── pr_summary/PR_SUMMARY.md
├── profile_dataset/profile.md, profile.json
├── data_quality/schema.py, run_validation.py
├── sql_refiner/query.sql, explain.sql, query_notes.md
├── schema_diff/migration.sql, migration.md
└── dbt_generator/models/...
```

> **Note:** The `./out/` directory is gitignored by default.

---

## Development

### Setup

```bash
# Clone and install
git clone https://github.com/your-org/skillpack.git
cd skillpack
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
pytest tests/ -v --cov=skillpack

# Run specific skill tests
pytest tests/test_profile_dataset.py -v
```

### Quality Checks

```bash
# Run full quality gate
make quality

# Individual checks
make format    # Auto-format code
make lint      # Run linter
make typecheck # Type checking
make test      # Run tests
```

### Adding a New Skill

1. Create `skillpack/skills/<skill_name>.py` with:
   - `register_parser(subparsers)` function
   - `handler(args)` function
   - Core logic functions

2. Add import and registration to `skillpack/cli.py`

3. Create documentation:
   - `skills/<skill_name>/SKILL.md`
   - `skills/<skill_name>/examples/`

4. Add tests: `tests/test_<skill_name>.py`

---

## VS Code Integration

Use the built-in VS Code tasks (Cmd+Shift+P → "Tasks: Run Task"):

- **skillpack: quality-gate** - Run quality checks
- **skillpack: project-scaffolding** - Generate new project
- **skillpack: profile-dataset** - Profile a CSV file
- **make: quality** - Full quality gate
- **make: test** - Run tests

---

## License

MIT License - see [LICENSE](LICENSE) for details.
