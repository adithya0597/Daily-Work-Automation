# dbt Generator Skill

## When to Use
- Creating new dbt project structure
- Generating staging models from sources
- Adding mart models with aggregations

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| config_path | file_path | No | dbt configuration YAML |

## Outputs
Directory structure in `./out/dbt_generator/`:
```
models/
├── staging/
│   └── stg_{source}.sql
├── marts/
│   └── {mart}.sql
├── schema.yml
└── docs.md
```

## Procedure
1. **Load config** - Parse YAML or use example
2. **Generate staging** - One model per source
3. **Generate marts** - Aggregation models
4. **Create schema.yml** - Tests and documentation
5. **Write outputs** - Save to ./out/

## Guardrails

### Allowed
- Read config file
- Generate SQL and YAML files
- Write to ./out/dbt_generator/

### Forbidden
- Execute dbt commands
- Connect to data warehouses
- Modify existing dbt projects
- Delete any files

## Preconditions
- [ ] Config is valid YAML (if provided)

## Postconditions
- [ ] All staging models created
- [ ] schema.yml has all models
- [ ] Generated SQL is valid

## Error Handling
| Error | Condition | Recovery |
|-------|-----------|----------|
| ConfigError | Invalid YAML | Fix YAML syntax |
| NoSources | No sources in config | Add sources section |

## Config Schema
```yaml
project_name: my_dbt_project
sources:
  - name: raw_db
    tables:
      - name: users
        columns: [id, name, email, created_at]
      - name: orders
        columns: [id, user_id, total, order_date]
marts:
  - name: daily_orders
    description: Daily order aggregations
    columns: [order_date, order_count, total_revenue]
```

## Generated Patterns

### Staging Model
```sql
WITH source AS (
    SELECT * FROM {{ source('raw_db', 'users') }}
),
renamed AS (
    SELECT id, name, email, created_at FROM source
)
SELECT * FROM renamed
```

### Mart Model
```sql
SELECT
    order_date,
    COUNT(*) AS order_count,
    SUM(total) AS total_revenue
FROM {{ ref('stg_orders') }}
GROUP BY order_date
```

## Examples
```bash
skillpack dbt-generator                       # Use example config
skillpack dbt-generator --config dbt.yaml     # Use custom config
```

## Related Skills
- **profile-dataset**: Profile source data first
- **data-quality**: Generate validation for sources
- **schema-diff**: Track schema changes
