#!/usr/bin/env python3
"""Profile CSV - Standalone script for CSV profiling.

This script can be run directly or called by the skillpack CLI.
It is designed to be agent-modifiable.

Usage:
    python profile_csv.py <csv_path> [--output-dir <dir>]
"""

import argparse
import csv
import json
import statistics
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def infer_dtype(values: list[str]) -> str:
    """Infer the data type from a list of string values."""
    non_empty = [v for v in values if v.strip()]
    if not non_empty:
        return "string"

    # Try integer
    try:
        for v in non_empty:
            int(v)
        return "integer"
    except ValueError:
        pass

    # Try float
    try:
        for v in non_empty:
            float(v)
        return "float"
    except ValueError:
        pass

    # Try boolean
    if all(v.lower() in ("true", "false", "yes", "no", "1", "0") for v in non_empty):
        return "boolean"

    return "string"


def profile_column(name: str, values: list[str]) -> dict[str, Any]:
    """Profile a single column."""
    total = len(values)
    non_empty = [v for v in values if v.strip()]
    null_count = total - len(non_empty)
    unique = set(non_empty)

    profile: dict[str, Any] = {
        "name": name,
        "dtype": infer_dtype(values),
        "total_count": total,
        "null_count": null_count,
        "null_rate": null_count / total if total > 0 else 0,
        "unique_count": len(unique),
        "sample_values": list(unique)[:5],
    }

    # Numeric statistics
    if profile["dtype"] in ("integer", "float"):
        try:
            nums = [float(v) for v in non_empty]
            profile["min_value"] = min(nums)
            profile["max_value"] = max(nums)
            profile["mean_value"] = statistics.mean(nums)
            profile["median_value"] = statistics.median(nums)
            if len(nums) >= 2:
                profile["std_dev"] = statistics.stdev(nums)
        except (ValueError, statistics.StatisticsError):
            pass

    # String statistics
    if profile["dtype"] == "string" and non_empty:
        lengths = [len(v) for v in non_empty]
        profile["min_length"] = min(lengths)
        profile["max_length"] = max(lengths)
        profile["avg_length"] = statistics.mean(lengths)

    return profile


def profile_csv(csv_path: Path) -> dict[str, Any]:
    """Profile an entire CSV file."""
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)

    columns_data: dict[str, list[str]] = {h: [] for h in headers}
    for row in rows:
        for h in headers:
            columns_data[h].append(row.get(h, ""))

    return {
        "file_path": str(csv_path.absolute()),
        "file_size_bytes": csv_path.stat().st_size,
        "row_count": len(rows),
        "column_count": len(headers),
        "profiled_at": datetime.now().isoformat(),
        "columns": [profile_column(h, columns_data[h]) for h in headers],
    }


def generate_markdown(profile: dict[str, Any]) -> str:
    """Generate markdown report from profile."""
    lines = [
        "# Dataset Profile",
        "",
        "## Overview",
        f"- **File:** `{profile['file_path']}`",
        f"- **Size:** {profile['file_size_bytes']} bytes",
        f"- **Rows:** {profile['row_count']}",
        f"- **Columns:** {profile['column_count']}",
        f"- **Profiled at:** {profile['profiled_at']}",
        "",
    ]

    for col in profile["columns"]:
        lines.extend([
            f"## {col['name']}",
            f"- **Type:** {col['dtype']}",
            f"- **Null Count:** {col['null_count']} ({col['null_rate']:.1%})",
            f"- **Unique Values:** {col['unique_count']}",
        ])

        if col["dtype"] in ("integer", "float"):
            if "min_value" in col:
                lines.append(f"- **Range:** [{col['min_value']}, {col['max_value']}]")
            if "mean_value" in col:
                lines.append(f"- **Mean:** {col['mean_value']:.2f}")

        if col["dtype"] == "string" and "min_length" in col:
            lines.append(f"- **Length Range:** [{col['min_length']}, {col['max_length']}]")

        lines.append(f"- **Samples:** {', '.join(col['sample_values'][:3])}")
        lines.append("")

    return "\n".join(lines)


def main(csv_path: str, output_dir: str = "./out/profile_dataset") -> int:
    """Main entry point."""
    path = Path(csv_path)
    if not path.exists():
        print(f"Error: File not found: {csv_path}", file=sys.stderr)
        return 1

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    profile = profile_csv(path)

    # Write JSON
    json_path = out_dir / "profile.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
    print(f"Wrote: {json_path}")

    # Write Markdown
    md_path = out_dir / "profile.md"
    md_path.write_text(generate_markdown(profile), encoding="utf-8")
    print(f"Wrote: {md_path}")

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Profile a CSV file")
    parser.add_argument("csv_path", help="Path to CSV file")
    parser.add_argument("--output-dir", default="./out/profile_dataset")
    args = parser.parse_args()
    sys.exit(main(args.csv_path, args.output_dir))
