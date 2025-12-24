"""git-workflow - Create feature branches, format commits, and generate PR templates."""

import argparse
import re
import subprocess
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import Any

from skillpack.utils.output import write_text


def handler(args: argparse.Namespace) -> int:
    """CLI handler for git-workflow."""
    action = args.action

    if action == "branch":
        result = create_branch(
            branch_type=args.type,
            description=args.description,
            issue=args.issue,
        )
    elif action == "commit":
        result = format_commit(
            commit_type=args.type,
            scope=args.scope,
            description=args.description,
            breaking=args.breaking,
        )
    elif action == "pr":
        result = generate_pr_template(
            title=args.title,
            branch=args.branch,
        )
    else:
        print(f"Unknown action: {action}")
        return 1

    if result.get("success"):
        print(f"✅ {result.get('message')}")
        if result.get("output"):
            print(f"\n{result['output']}")
        return 0
    print(f"❌ Error: {result.get('error')}")
    return 1


def register_parser(subparsers: Any) -> None:
    """Register the git-workflow subcommand."""
    parser = subparsers.add_parser(
        "git-workflow",
        help="Create feature branches, format commits, and generate PR templates",
    )

    subparsers_action = parser.add_subparsers(
        dest="action",
        title="actions",
        description="Git workflow actions",
    )

    # Branch subcommand
    branch_parser = subparsers_action.add_parser(
        "branch",
        help="Create a properly named feature branch",
    )
    branch_parser.add_argument(
        "--type",
        choices=["feature", "bugfix", "hotfix", "release", "chore"],
        default="feature",
        help="Branch type",
    )
    branch_parser.add_argument(
        "--description",
        required=True,
        help="Brief description (will be slugified)",
    )
    branch_parser.add_argument(
        "--issue",
        help="Issue/ticket number (e.g., JIRA-123)",
    )

    # Commit subcommand
    commit_parser = subparsers_action.add_parser(
        "commit",
        help="Format a conventional commit message",
    )
    commit_parser.add_argument(
        "--type",
        choices=["feat", "fix", "docs", "style", "refactor", "test", "chore", "perf", "ci"],
        default="feat",
        help="Commit type",
    )
    commit_parser.add_argument(
        "--scope",
        help="Scope of the change",
    )
    commit_parser.add_argument(
        "--description",
        required=True,
        help="Commit description",
    )
    commit_parser.add_argument(
        "--breaking",
        action="store_true",
        help="Mark as breaking change",
    )

    # PR subcommand
    pr_parser = subparsers_action.add_parser(
        "pr",
        help="Generate a PR template",
    )
    pr_parser.add_argument(
        "--title",
        required=True,
        help="PR title",
    )
    pr_parser.add_argument(
        "--branch",
        help="Branch name (defaults to current)",
    )

    parser.set_defaults(handler=handler)


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")


def get_current_branch() -> str:
    """Get current git branch name."""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "unknown"


def create_branch(
    branch_type: str,
    description: str,
    issue: str | None = None,
) -> dict[str, Any]:
    """Create a properly named feature branch."""
    slug = slugify(description)

    if issue:
        branch_name = f"{branch_type}/{issue}-{slug}"
    else:
        branch_name = f"{branch_type}/{slug}"

    # Limit length
    if len(branch_name) > 50:
        branch_name = branch_name[:50].rstrip("-")

    return {
        "success": True,
        "message": f"Branch name generated",
        "output": f"git checkout -b {branch_name}",
        "branch_name": branch_name,
    }


def format_commit(
    commit_type: str,
    description: str,
    scope: str | None = None,
    breaking: bool = False,
) -> dict[str, Any]:
    """Format a conventional commit message."""
    # Build commit message
    if scope:
        prefix = f"{commit_type}({scope})"
    else:
        prefix = commit_type

    if breaking:
        prefix = f"{prefix}!"

    commit_message = f"{prefix}: {description}"

    return {
        "success": True,
        "message": "Commit message formatted",
        "output": f'git commit -m "{commit_message}"',
        "commit_message": commit_message,
    }


def generate_pr_template(
    title: str,
    branch: str | None = None,
) -> dict[str, Any]:
    """Generate a PR template."""
    if branch is None:
        branch = get_current_branch()

    template = dedent(f"""\
        # {title}

        ## Summary
        <!-- Brief description of changes -->

        ## Changes Made
        - [ ] TODO: List changes

        ## Testing
        - [ ] Tests pass locally
        - [ ] New tests added (if applicable)

        ## Checklist
        - [ ] Code follows project style guidelines
        - [ ] Documentation updated
        - [ ] No breaking changes (or documented below)

        ## Related Issues
        <!-- Link any related issues -->

        ## Screenshots (if applicable)
        <!-- Add screenshots -->

        ---
        Branch: `{branch}`
        Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
    """)

    pr_file = write_text(
        content=template,
        filename="PR_TEMPLATE.md",
        skill_name="git_workflow",
    )

    return {
        "success": True,
        "message": f"PR template generated at {pr_file}",
        "output": template,
        "file": str(pr_file),
    }
