"""Profile Dataset Skill - Profile CSV datasets."""

import argparse
import csv
import json
import statistics
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from skillpack.utils.logging import get_logger
from skillpack.utils.output import get_output_dir

SKILL_NAME = "profile_dataset"


@dataclass
class ColumnProfile:
    """Profile for a single column."""

    name: str
    dtype: str
    total_count: int
    null_count: int
    unique_count: int
    sample_values: list[str]
    # Numeric stats (if applicable)
    min_value: float | None = None
    max_value: float | None = None
    mean_value: float | None = None
    median_value: float | None = None
    std_dev: float | None = None
    # String stats (if applicable)
    min_length: int | None = None
    max_length: int | None = None
    avg_length: float | None = None


@dataclass
class DatasetProfile:
    """Profile for an entire dataset."""

    file_path: str
    file_size_bytes: int
    row_count: int
    column_count: int
    columns: list[ColumnProfile] = field(default_factory=list)
    profiled_at: str = field(default_factory=lambda: datetime.now().isoformat())


def infer_dtype(values: list[str]) -> str:
    """Infer the data type from a list of string values.

    Args:
        values: List of string values.

    Returns:
        Inferred type: 'integer', 'float', 'boolean', or 'string'.
    """
    non_empty = [v for v in values if v.strip()]
    if not non_empty:
        return "string"

    # Check for boolean
    bool_values = {"true", "false", "yes", "no", "1", "0", "t", "f", "y", "n"}
    if all(v.lower() in bool_values for v in non_empty):
        return "boolean"

    # Check for integer
    try:
        for v in non_empty:
            int(v)
        return "integer"
    except ValueError:
        pass

    # Check for float
    try:
        for v in non_empty:
            float(v)
        return "float"
    except ValueError:
        pass

    return "string"


def profile_column(name: str, values: list[str]) -> ColumnProfile:
    """Profile a single column.

    Args:
        name: Column name.
        values: List of values in the column.

    Returns:
        ColumnProfile with statistics.
    """
    total_count = len(values)
    null_count = sum(1 for v in values if not v.strip())
    non_null_values = [v for v in values if v.strip()]
    unique_count = len(set(non_null_values))

    # Get sample values (up to 5 unique values)
    sample_values = list(set(non_null_values))[:5]

    dtype = infer_dtype(non_null_values)

    profile = ColumnProfile(
        name=name,
        dtype=dtype,
        total_count=total_count,
        null_count=null_count,
        unique_count=unique_count,
        sample_values=sorted(sample_values),
    )

    # Compute numeric stats
    if dtype in ("integer", "float") and non_null_values:
        try:
            numeric_values = [float(v) for v in non_null_values]
            profile.min_value = min(numeric_values)
            profile.max_value = max(numeric_values)
            profile.mean_value = statistics.mean(numeric_values)
            profile.median_value = statistics.median(numeric_values)
            if len(numeric_values) > 1:
                profile.std_dev = statistics.stdev(numeric_values)
        except (ValueError, statistics.StatisticsError):
            pass

    # Compute string stats
    if dtype == "string" and non_null_values:
        lengths = [len(v) for v in non_null_values]
        profile.min_length = min(lengths)
        profile.max_length = max(lengths)
        profile.avg_length = statistics.mean(lengths)

    return profile


def profile_csv(csv_path: str | Path) -> DatasetProfile:
    """Profile a CSV file.

    Args:
        csv_path: Path to the CSV file.

    Returns:
        DatasetProfile with all column profiles.
    """
    logger = get_logger()
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    logger.info(f"Profiling: {csv_path}")

    # Read CSV
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV file has no headers")

        headers = list(reader.fieldnames)
        rows = list(reader)

    # Collect values per column
    column_values: dict[str, list[str]] = {h: [] for h in headers}
    for row in rows:
        for h in headers:
            column_values[h].append(row.get(h, ""))

    # Profile each column
    columns = [profile_column(h, column_values[h]) for h in headers]

    return DatasetProfile(
        file_path=str(csv_path.absolute()),
        file_size_bytes=csv_path.stat().st_size,
        row_count=len(rows),
        column_count=len(headers),
        columns=columns,
    )


def profile_to_dict(profile: DatasetProfile) -> dict[str, Any]:
    """Convert a DatasetProfile to a dictionary.

    Args:
        profile: The profile to convert.

    Returns:
        Dictionary representation of the profile.
    """
    return {
        "file_path": profile.file_path,
        "file_size_bytes": profile.file_size_bytes,
        "row_count": profile.row_count,
        "column_count": profile.column_count,
        "profiled_at": profile.profiled_at,
        "columns": [
            {
                "name": col.name,
                "dtype": col.dtype,
                "total_count": col.total_count,
                "null_count": col.null_count,
                "null_rate": round(col.null_count / col.total_count, 4) if col.total_count else 0,
                "unique_count": col.unique_count,
                "sample_values": col.sample_values,
                "min_value": col.min_value,
                "max_value": col.max_value,
                "mean_value": round(col.mean_value, 4) if col.mean_value else None,
                "median_value": col.median_value,
                "std_dev": round(col.std_dev, 4) if col.std_dev else None,
                "min_length": col.min_length,
                "max_length": col.max_length,
                "avg_length": round(col.avg_length, 2) if col.avg_length else None,
            }
            for col in profile.columns
        ],
    }


def profile_to_markdown(profile: DatasetProfile) -> str:
    """Convert a DatasetProfile to markdown.

    Args:
        profile: The profile to convert.

    Returns:
        Markdown representation of the profile.
    """
    lines = [
        "# Dataset Profile",
        "",
        "## Overview",
        "",
        f"- **File:** `{profile.file_path}`",
        f"- **Size:** {profile.file_size_bytes:,} bytes",
        f"- **Rows:** {profile.row_count:,}",
        f"- **Columns:** {profile.column_count}",
        f"- **Profiled at:** {profile.profiled_at}",
        "",
        "## Columns",
        "",
    ]

    for col in profile.columns:
        null_rate = (col.null_count / col.total_count * 100) if col.total_count else 0
        lines.extend([
            f"### {col.name}",
            "",
            f"- **Type:** {col.dtype}",
            f"- **Null Count:** {col.null_count} ({null_rate:.1f}%)",
            f"- **Unique Values:** {col.unique_count}",
        ])

        if col.dtype in ("integer", "float"):
            lines.append(f"- **Range:** [{col.min_value}, {col.max_value}]")
            if col.mean_value is not None:
                lines.append(f"- **Mean:** {col.mean_value:.4f}")
            if col.median_value is not None:
                lines.append(f"- **Median:** {col.median_value}")
            if col.std_dev is not None:
                lines.append(f"- **Std Dev:** {col.std_dev:.4f}")

        if col.dtype == "string" and col.min_length is not None:
            lines.append(f"- **Length Range:** [{col.min_length}, {col.max_length}]")
            if col.avg_length is not None:
                lines.append(f"- **Avg Length:** {col.avg_length:.2f}")

        if col.sample_values:
            samples = ", ".join(f"`{v}`" for v in col.sample_values[:5])
            lines.append(f"- **Sample Values:** {samples}")

        lines.append("")

    return "\n".join(lines)


def generate_profile(
    csv_path: str,
    base_dir: str = "./out",
) -> tuple[Path, Path]:
    """Generate profile outputs for a CSV file.

    Args:
        csv_path: Path to the CSV file.
        base_dir: Base output directory.

    Returns:
        Tuple of (markdown_path, json_path).
    """
    logger = get_logger()

    profile = profile_csv(csv_path)
    profile_dict = profile_to_dict(profile)
    profile_md = profile_to_markdown(profile)

    output_dir = get_output_dir(SKILL_NAME, base_dir)

    # Write JSON
    json_path = output_dir / "profile.json"
    json_path.write_text(
        json.dumps(profile_dict, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    logger.info(f"JSON profile: {json_path}")

    # Write Markdown
    md_path = output_dir / "profile.md"
    md_path.write_text(profile_md, encoding="utf-8")
    logger.info(f"Markdown profile: {md_path}")

    return md_path, json_path


def handler(args: argparse.Namespace) -> int:
    """Handle the profile-dataset command."""
    try:
        md_path, json_path = generate_profile(csv_path=args.csv)
        print(f"✅ Profile generated:")
        print(f"   Markdown: {md_path}")
        print(f"   JSON: {json_path}")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def register_parser(subparsers: Any) -> None:
    """Register the profile-dataset subcommand."""
    parser = subparsers.add_parser(
        "profile-dataset",
        help="Profile a CSV dataset",
        description="Profiles a CSV file and generates statistics in markdown and JSON formats.",
    )
    parser.add_argument(
        "--csv",
        required=True,
        help="Path to the CSV file to profile",
    )
    parser.set_defaults(handler=handler)
