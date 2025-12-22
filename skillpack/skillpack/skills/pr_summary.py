"""PR Summary Skill - Generate PR summaries with risk assessment from diffs."""

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from skillpack.utils.logging import get_logger
from skillpack.utils.output import get_output_dir, write_text

SKILL_NAME = "pr_summary"


@dataclass
class DiffStats:
    """Statistics extracted from a diff."""

    files_changed: list[str]
    insertions: int
    deletions: int
    binary_files: list[str]
    file_types: dict[str, int]


def parse_diff(diff_content: str) -> DiffStats:
    """Parse a unified diff and extract statistics.

    Args:
        diff_content: Content of the diff file.

    Returns:
        DiffStats with extracted information.
    """
    files_changed: list[str] = []
    binary_files: list[str] = []
    insertions = 0
    deletions = 0
    file_types: dict[str, int] = {}

    # Match file headers in unified diff format
    file_pattern = re.compile(r"^(?:diff --git a/(.+?) b/|--- a/(.+)|--- (.+))$", re.MULTILINE)
    binary_pattern = re.compile(r"^Binary files .+ and .+ differ$", re.MULTILINE)

    for match in file_pattern.finditer(diff_content):
        filename = match.group(1) or match.group(2) or match.group(3)
        if filename and filename not in files_changed and not filename.startswith("/dev/null"):
            files_changed.append(filename)

            # Track file types
            ext = Path(filename).suffix.lower() or "(no ext)"
            file_types[ext] = file_types.get(ext, 0) + 1

    for match in binary_pattern.finditer(diff_content):
        # Extract binary file names if needed
        binary_files.append("(binary)")

    # Count insertions and deletions
    for line in diff_content.split("\n"):
        if line.startswith("+") and not line.startswith("+++"):
            insertions += 1
        elif line.startswith("-") and not line.startswith("---"):
            deletions += 1

    return DiffStats(
        files_changed=sorted(files_changed),
        insertions=insertions,
        deletions=deletions,
        binary_files=binary_files,
        file_types=dict(sorted(file_types.items())),
    )


def assess_risk(stats: DiffStats) -> tuple[str, list[str]]:
    """Assess the risk level of changes.

    Args:
        stats: Diff statistics.

    Returns:
        Tuple of (risk_level, risk_factors).
    """
    risk_factors: list[str] = []
    risk_score = 0

    # Large changes
    total_changes = stats.insertions + stats.deletions
    if total_changes > 500:
        risk_factors.append(f"Large change: {total_changes} lines modified")
        risk_score += 2
    elif total_changes > 200:
        risk_factors.append(f"Medium-sized change: {total_changes} lines modified")
        risk_score += 1

    # Many files changed
    if len(stats.files_changed) > 20:
        risk_factors.append(f"Many files changed: {len(stats.files_changed)}")
        risk_score += 2
    elif len(stats.files_changed) > 10:
        risk_factors.append(f"Multiple files changed: {len(stats.files_changed)}")
        risk_score += 1

    # Sensitive file types
    sensitive_patterns = {
        ".sql": "Database schema changes",
        ".env": "Environment configuration changes",
        ".yml": "CI/CD or config changes",
        ".yaml": "CI/CD or config changes",
        "migration": "Database migration",
    }

    for pattern, description in sensitive_patterns.items():
        for filename in stats.files_changed:
            if pattern in filename.lower():
                risk_factors.append(description)
                risk_score += 1
                break

    # Determine risk level
    if risk_score >= 4:
        risk_level = "🔴 HIGH"
    elif risk_score >= 2:
        risk_level = "🟡 MEDIUM"
    else:
        risk_level = "🟢 LOW"

    return risk_level, risk_factors


def generate_summary(
    diff_content: str,
    title: str = "Pull Request Summary",
) -> str:
    """Generate a PR summary markdown document.

    Args:
        diff_content: Content of the diff.
        title: Title for the summary.

    Returns:
        Markdown content for the PR summary.
    """
    stats = parse_diff(diff_content)
    risk_level, risk_factors = assess_risk(stats)

    # Build the summary
    lines = [
        f"# {title}",
        "",
        "## Overview",
        "",
        f"- **Files Changed:** {len(stats.files_changed)}",
        f"- **Lines Added:** +{stats.insertions}",
        f"- **Lines Removed:** -{stats.deletions}",
        "",
        "## Risk Assessment",
        "",
        f"**Risk Level:** {risk_level}",
        "",
    ]

    if risk_factors:
        lines.append("### Risk Factors")
        lines.append("")
        for factor in risk_factors:
            lines.append(f"- {factor}")
        lines.append("")

    # File types breakdown
    if stats.file_types:
        lines.append("## File Types Changed")
        lines.append("")
        for ext, count in stats.file_types.items():
            lines.append(f"- `{ext}`: {count} file(s)")
        lines.append("")

    # Files list
    lines.append("## Files Changed")
    lines.append("")
    for filename in stats.files_changed[:50]:  # Limit to 50 files
        lines.append(f"- `{filename}`")
    if len(stats.files_changed) > 50:
        lines.append(f"- ... and {len(stats.files_changed) - 50} more files")
    lines.append("")

    # Rollout/Rollback guidance
    lines.extend([
        "## Rollout Plan",
        "",
        "1. Merge to main branch",
        "2. Deploy to staging environment",
        "3. Run smoke tests",
        "4. Deploy to production",
        "",
        "## Rollback Plan",
        "",
        "1. Revert the merge commit: `git revert <commit-sha>`",
        "2. Push the revert",
        "3. Deploy the reverted code",
        "",
        "## Testing Checklist",
        "",
        "- [ ] Unit tests pass",
        "- [ ] Integration tests pass",
        "- [ ] Manual testing completed",
        "- [ ] Performance impact assessed",
        "",
    ])

    return "\n".join(lines)


def generate_pr_summary(
    diff_file: str | None = None,
    diff_content: str | None = None,
    title: str = "Pull Request Summary",
    base_dir: str = "./out",
) -> Path:
    """Generate a PR summary from a diff.

    Args:
        diff_file: Path to a diff file.
        diff_content: Direct diff content (alternative to diff_file).
        title: Title for the summary.
        base_dir: Base output directory.

    Returns:
        Path to the generated PR summary.
    """
    logger = get_logger()

    if diff_file:
        diff_path = Path(diff_file)
        if not diff_path.exists():
            raise FileNotFoundError(f"Diff file not found: {diff_file}")
        content = diff_path.read_text(encoding="utf-8")
    elif diff_content:
        content = diff_content
    else:
        raise ValueError("Either diff_file or diff_content must be provided")

    logger.info("Generating PR summary...")
    summary = generate_summary(content, title)

    output_dir = get_output_dir(SKILL_NAME, base_dir)
    output_path = output_dir / "PR_SUMMARY.md"
    output_path.write_text(summary, encoding="utf-8")

    logger.info(f"PR summary generated: {output_path}")
    return output_path


def handler(args: argparse.Namespace) -> int:
    """Handle the pr-summary command."""
    try:
        output_path = generate_pr_summary(
            diff_file=args.diff_file,
            title=args.title,
        )
        print(f"✅ PR summary generated: {output_path}")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def register_parser(subparsers: Any) -> None:
    """Register the pr-summary subcommand."""
    parser = subparsers.add_parser(
        "pr-summary",
        help="Generate PR summary with risk assessment",
        description="Generates a PR summary with changes, risk assessment, and rollout plan.",
    )
    parser.add_argument(
        "--diff-file",
        required=True,
        help="Path to the diff file to analyze",
    )
    parser.add_argument(
        "--title",
        default="Pull Request Summary",
        help="Title for the summary (default: 'Pull Request Summary')",
    )
    parser.set_defaults(handler=handler)
