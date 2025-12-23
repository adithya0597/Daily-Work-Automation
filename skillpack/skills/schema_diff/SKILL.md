# Schema Diff Skill

## When to Use
- Planning database migrations
- Comparing schema versions
- Generating ALTER statements

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| old_schema | file_path | Yes | Old schema JSON |
| new_schema | file_path | Yes | New schema JSON |
| table_name | string | No | Table name for SQL |

## Outputs
- `migration.sql` - Forward + rollback SQL
- `migration.md` - Impact documentation

## Procedure
1. **Parse schemas** - Load JSON, extract columns
2. **Compare** - Find added, removed, modified
3. **Generate SQL** - ALTER TABLE statements
4. **Assess impact** - Document risks
5. **Write outputs** - Save to ./out/

## Guardrails
### Allowed
- Read schema JSON files
- Generate SQL migration code
- Write to ./out/schema_diff/

### Forbidden
- Execute SQL migrations
- Connect to databases

## Example
```bash
skillpack schema-diff --old v1.json --new v2.json --table users
```
