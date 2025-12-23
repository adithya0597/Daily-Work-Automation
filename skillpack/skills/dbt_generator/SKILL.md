# dbt Generator Skill

## When to Use
- Creating new dbt project structure
- Generating staging models from sources
- Adding mart models with aggregations

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| config_path | file_path | No | dbt config YAML |

## Outputs
Directory structure in `./out/dbt_generator/`:
- models/staging/*.sql
- models/marts/*.sql
- models/schema.yml
- models/docs.md

## Procedure
1. **Load config** - Parse YAML or use example
2. **Generate staging** - One model per source
3. **Generate marts** - Aggregation models
4. **Create schema.yml** - Tests and docs
5. **Write outputs** - Save to ./out/

## Guardrails
### Allowed
- Read config file
- Generate SQL and YAML files
- Write to ./out/dbt_generator/

### Forbidden
- Execute dbt commands
- Connect to warehouses

## Example
```bash
skillpack dbt-generator --config dbt_config.yaml
```
