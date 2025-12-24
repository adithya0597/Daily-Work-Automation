"""daily-ops-summary - Generate daily status report from pipeline and system health."""

import argparse
from datetime import datetime, timedelta
from pathlib import Path
from textwrap import dedent
from typing import Any

import yaml

from skillpack.utils.output import get_output_dir, write_text


def handler(args: argparse.Namespace) -> int:
    """CLI handler for daily-ops-summary."""
    # Load metrics if provided
    metrics = {}
    if args.metrics and args.metrics.exists():
        with open(args.metrics) as f:
            metrics = yaml.safe_load(f) or {}

    result = daily_ops_summary_main(
        date=args.date,
        metrics=metrics,
        team=args.team,
        output_dir=args.output_dir,
    )

    if result.get("success"):
        print(f"✅ Generated daily summary: {result['summary_file']}")
        return 0
    print(f"❌ Error: {result.get('error')}")
    return 1


def register_parser(subparsers: Any) -> None:
    """Register the daily-ops-summary subcommand."""
    parser = subparsers.add_parser(
        "daily-ops-summary",
        help="Generate daily status report from pipeline and system health",
    )
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Date for summary (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--metrics",
        type=Path,
        help="Path to metrics YAML file",
    )
    parser.add_argument(
        "--team",
        default="Data Platform",
        help="Team name for the report",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./out/daily_ops_summary"),
        help="Output directory",
    )
    parser.set_defaults(handler=handler)


def daily_ops_summary_main(
    date: str | None = None,
    metrics: dict | None = None,
    team: str = "Data Platform",
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """Generate daily operations summary."""
    if output_dir is None:
        output_dir = get_output_dir("daily_ops_summary")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    if metrics is None:
        metrics = generate_sample_metrics()

    try:
        # Generate summary report
        summary = generate_summary(date, metrics, team)
        summary_file = write_text(
            content=summary, filename=f"ops_summary_{date}.md", skill_name="daily_ops_summary"
        )

        # Generate Slack message
        slack_msg = generate_slack_message(date, metrics, team)
        write_text(
            content=slack_msg, filename=f"slack_message_{date}.txt", skill_name="daily_ops_summary"
        )

        # Generate metrics YAML
        metrics_yaml = generate_metrics_yaml(date, metrics)
        write_text(
            content=metrics_yaml, filename=f"metrics_{date}.yaml", skill_name="daily_ops_summary"
        )

        return {
            "success": True,
            "summary_file": str(summary_file),
            "output_dir": str(output_dir),
            "files": [
                f"ops_summary_{date}.md",
                f"slack_message_{date}.txt",
                f"metrics_{date}.yaml",
            ],
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_sample_metrics() -> dict:
    """Generate sample metrics for demo."""
    return {
        "pipelines": {
            "total": 45,
            "succeeded": 42,
            "failed": 2,
            "running": 1,
            "success_rate": 95.6,
        },
        "jobs": {
            "completed": 1250,
            "failed": 15,
            "avg_duration_min": 12.5,
        },
        "data": {
            "rows_processed": 15_000_000,
            "tables_updated": 85,
            "data_freshness_hours": 1.2,
        },
        "alerts": {
            "critical": 0,
            "warning": 3,
            "info": 12,
        },
        "sla": {
            "met": 98.5,
            "breached": ["marketing_daily_rollup"],
        },
        "resources": {
            "cpu_avg_pct": 45,
            "memory_avg_pct": 62,
            "storage_used_pct": 78,
        },
        "incidents": [],
    }


def generate_summary(date: str, metrics: dict, team: str) -> str:
    """Generate markdown summary."""
    
    pipelines = metrics.get("pipelines", {})
    jobs = metrics.get("jobs", {})
    data = metrics.get("data", {})
    alerts = metrics.get("alerts", {})
    sla = metrics.get("sla", {})
    resources = metrics.get("resources", {})
    incidents = metrics.get("incidents", [])

    # Calculate health status
    success_rate = pipelines.get("success_rate", 100)
    if success_rate >= 98:
        health_emoji = "🟢"
        health_status = "Healthy"
    elif success_rate >= 95:
        health_emoji = "🟡"
        health_status = "Degraded"
    else:
        health_emoji = "🔴"
        health_status = "Critical"

    # SLA breaches
    sla_breaches = sla.get("breached", [])
    sla_section = (
        "\n".join([f"- ⚠️ `{b}`" for b in sla_breaches])
        if sla_breaches
        else "✅ All SLAs met"
    )

    # Incidents
    incident_section = (
        "\n".join([f"- 🚨 {i}" for i in incidents])
        if incidents
        else "✅ No incidents"
    )

    return dedent(f'''\
        # {team} Daily Operations Summary

        **Date**: {date}  
        **Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M")}  
        **Status**: {health_emoji} {health_status}

        ---

        ## 📊 Pipeline Health

        | Metric | Value |
        |--------|-------|
        | Total Pipelines | {pipelines.get("total", 0)} |
        | Succeeded | {pipelines.get("succeeded", 0)} ✅ |
        | Failed | {pipelines.get("failed", 0)} ❌ |
        | Running | {pipelines.get("running", 0)} 🔄 |
        | Success Rate | {pipelines.get("success_rate", 0):.1f}% |

        ## 📈 Job Metrics

        | Metric | Value |
        |--------|-------|
        | Jobs Completed | {jobs.get("completed", 0):,} |
        | Jobs Failed | {jobs.get("failed", 0)} |
        | Avg Duration | {jobs.get("avg_duration_min", 0):.1f} min |

        ## 📦 Data Processing

        | Metric | Value |
        |--------|-------|
        | Rows Processed | {data.get("rows_processed", 0):,} |
        | Tables Updated | {data.get("tables_updated", 0)} |
        | Data Freshness | {data.get("data_freshness_hours", 0):.1f} hours |

        ## 🚨 Alerts

        | Severity | Count |
        |----------|-------|
        | Critical | {alerts.get("critical", 0)} |
        | Warning | {alerts.get("warning", 0)} |
        | Info | {alerts.get("info", 0)} |

        ## 🎯 SLA Status

        **SLA Met**: {sla.get("met", 100):.1f}%

        {sla_section}

        ## 💻 Resources

        | Resource | Usage |
        |----------|-------|
        | CPU (avg) | {resources.get("cpu_avg_pct", 0)}% |
        | Memory (avg) | {resources.get("memory_avg_pct", 0)}% |
        | Storage | {resources.get("storage_used_pct", 0)}% |

        ## 🔥 Incidents

        {incident_section}

        ---

        ## Action Items

        {"- [ ] Investigate failed pipelines" if pipelines.get("failed", 0) > 0 else ""}
        {"- [ ] Review SLA breaches" if sla_breaches else ""}
        {"- [ ] Address critical alerts" if alerts.get("critical", 0) > 0 else ""}
        {"- [ ] Monitor storage usage" if resources.get("storage_used_pct", 0) > 80 else ""}
        {"✅ No immediate action required" if pipelines.get("failed", 0) == 0 and not sla_breaches and alerts.get("critical", 0) == 0 else ""}
    ''')


def generate_slack_message(date: str, metrics: dict, team: str) -> str:
    """Generate Slack-formatted message."""
    
    pipelines = metrics.get("pipelines", {})
    success_rate = pipelines.get("success_rate", 100)
    
    if success_rate >= 98:
        emoji = "✅"
        status = "All systems healthy"
    elif success_rate >= 95:
        emoji = "⚠️"
        status = "Minor issues detected"
    else:
        emoji = "🔴"
        status = "Action required"

    return dedent(f'''\
        {emoji} *{team} Daily Ops Summary - {date}*

        *Pipeline Status*
        • Total: {pipelines.get("total", 0)} | ✅ {pipelines.get("succeeded", 0)} | ❌ {pipelines.get("failed", 0)}
        • Success Rate: {success_rate:.1f}%

        *Data Processing*
        • Rows: {metrics.get("data", {}).get("rows_processed", 0):,}
        • Tables: {metrics.get("data", {}).get("tables_updated", 0)}

        *Alerts*
        • Critical: {metrics.get("alerts", {}).get("critical", 0)} | Warning: {metrics.get("alerts", {}).get("warning", 0)}

        *Status*: {status}

        _View full report: ./out/daily_ops_summary/ops_summary_{date}.md_
    ''')


def generate_metrics_yaml(date: str, metrics: dict) -> str:
    """Generate metrics YAML file."""
    output = {
        "date": date,
        "generated_at": datetime.now().isoformat(),
        "metrics": metrics,
    }
    return yaml.dump(output, default_flow_style=False)
