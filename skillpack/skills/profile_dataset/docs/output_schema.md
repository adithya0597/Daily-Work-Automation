# Output Schema

## profile.json Structure

```json
{
  "file_path": "string - absolute path to profiled file",
  "file_size_bytes": "integer",
  "row_count": "integer",
  "column_count": "integer",
  "profiled_at": "ISO8601 datetime",
  "columns": [
    {
      "name": "string",
      "dtype": "integer | float | string | boolean",
      "total_count": "integer",
      "null_count": "integer",
      "null_rate": "float (0.0-1.0)",
      "unique_count": "integer",
      "sample_values": ["string array, max 5"],
      "min_value": "number (nullable, numeric only)",
      "max_value": "number (nullable, numeric only)",
      "mean_value": "number (nullable, numeric only)",
      "median_value": "number (nullable, numeric only)",
      "std_dev": "number (nullable, numeric only)",
      "min_length": "integer (nullable, strings only)",
      "max_length": "integer (nullable, strings only)",
      "avg_length": "float (nullable, strings only)"
    }
  ]
}
```

## Statistics Computed

### All Columns
- `total_count` - Total number of rows
- `null_count` - Count of null/empty values
- `unique_count` - Count of distinct values
- `sample_values` - Up to 5 unique sample values

### Numeric Columns Only
- `min_value` - Minimum value
- `max_value` - Maximum value
- `mean_value` - Arithmetic mean
- `median_value` - Median (50th percentile)
- `std_dev` - Standard deviation

### String Columns Only
- `min_length` - Shortest string length
- `max_length` - Longest string length
- `avg_length` - Average string length
