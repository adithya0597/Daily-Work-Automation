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
| table_name | string | No | Table name for SQL (default: table_name) |

## Outputs
- `./out/schema_diff/migration.sql` - Forward + rollback SQL
- `./out/schema_diff/migration.md` - Impact documentation

## Procedure
1. **Parse schemas** - Load JSON, extract columns
2. **Compare** - Find added, removed, modified columns
3. **Generate SQL** - ALTER TABLE statements
4. **Assess impact** - Document risks and considerations
5. **Write outputs** - Save to ./out/

## Guardrails

### Allowed
- Read schema JSON files
- Generate SQL migration code
- Write to ./out/schema_diff/

### Forbidden
- Execute SQL migrations
- Connect to databases
- Modify input schema files
- Delete any files

## Preconditions
- [ ] Both schema files exist
- [ ] Schemas are valid JSON

## Postconditions
- [ ] migration.sql has forward statements
- [ ] migration.sql has rollback statements
- [ ] migration.md documents changes

## Error Handling
| Error | Condition | Recovery |
|-------|-----------|----------|
| FileNotFoundError | Schema missing | Check paths |
| InvalidJSON | Schema malformed | Fix JSON syntax |

## Schema Format
```json
{
  "columns": {
    "id": {"type": "integer", "nullable": false},
    "name": {"type": "varchar(255)", "nullable": true}
  }
}
```

## Change Types
| Change | Risk | SQL |
|--------|------|-----|
| Add column | Low | `ALTER TABLE ADD COLUMN` |
| Remove column | High | `ALTER TABLE DROP COLUMN` |
| Modify type | Medium | `ALTER TABLE ALTER COLUMN` |
| Add NOT NULL | High | Requires default value |

## Examples
```bash
skillpack schema-diff --old v1.json --new v2.json
skillpack schema-diff --old v1.json --new v2.json --table users
```

## Related Skills
- **profile-dataset**: Understand data before migration
- **dbt-generator**: Generate models from schema
