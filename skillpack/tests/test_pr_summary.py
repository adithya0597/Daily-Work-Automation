"""Tests for pr_summary skill."""

from pathlib import Path

import pytest

from skillpack.skills.pr_summary import (
    DiffStats,
    assess_risk,
    generate_pr_summary,
    generate_summary,
    parse_diff,
)


SAMPLE_DIFF = """diff --git a/src/main.py b/src/main.py
index abc1234..def5678 100644
--- a/src/main.py
+++ b/src/main.py
@@ -1,5 +1,10 @@
 def main():
-    print("hello")
+    print("hello world")
+    return 0
+
+def helper():
+    pass
"""


def test_parse_diff_extracts_files() -> None:
    """Test that parse_diff extracts file names."""
    stats = parse_diff(SAMPLE_DIFF)
    assert "src/main.py" in stats.files_changed


def test_parse_diff_counts_changes() -> None:
    """Test that parse_diff counts insertions and deletions."""
    stats = parse_diff(SAMPLE_DIFF)
    assert stats.insertions > 0
    assert stats.deletions > 0


def test_assess_risk_low() -> None:
    """Test risk assessment for small changes."""
    stats = DiffStats(
        files_changed=["file1.py"],
        insertions=10,
        deletions=5,
        binary_files=[],
        file_types={".py": 1},
    )
    level, factors = assess_risk(stats)
    assert "LOW" in level


def test_assess_risk_high() -> None:
    """Test risk assessment for large changes."""
    stats = DiffStats(
        files_changed=[f"file{i}.py" for i in range(25)],
        insertions=500,
        deletions=200,
        binary_files=[],
        file_types={".py": 25},
    )
    level, factors = assess_risk(stats)
    assert "HIGH" in level or "MEDIUM" in level


def test_generate_summary_creates_markdown() -> None:
    """Test that generate_summary creates valid markdown."""
    summary = generate_summary(SAMPLE_DIFF)
    assert "# " in summary  # Has heading
    assert "Risk" in summary
    assert "Files Changed" in summary


def test_generate_pr_summary_creates_file(tmp_path: Path) -> None:
    """Test that generate_pr_summary creates output file."""
    diff_file = tmp_path / "test.diff"
    diff_file.write_text(SAMPLE_DIFF)

    output_path = generate_pr_summary(
        diff_file=str(diff_file),
        base_dir=str(tmp_path / "out"),
    )

    assert output_path.exists()
    assert output_path.name == "PR_SUMMARY.md"
