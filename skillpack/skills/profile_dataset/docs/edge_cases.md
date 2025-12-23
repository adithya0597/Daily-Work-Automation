# Edge Cases and Special Handling

## Encoding Issues
- Default: UTF-8
- If UnicodeDecodeError: try ISO-8859-1
- Pass explicit encoding if known

## Empty Values
- Empty string `""` → treated as null
- String `"null"` or `"NULL"` → left as string
- `NaN` → treated as null for numeric

## Large Files
- Files > 100MB: warn user, profile may be slow
- Consider sampling first N rows for large files

## No Headers
- First row assumed to be headers
- If no headers: auto-generate Column_0, Column_1, etc.

## Mixed Types
- Column with mixed int/float → float
- Column with mixed numbers/strings → string
- Sample values show type diversity

## Date Detection
- Common formats: YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY
- Not currently parsed as dates (listed as strings)
- Future: add date type inference
