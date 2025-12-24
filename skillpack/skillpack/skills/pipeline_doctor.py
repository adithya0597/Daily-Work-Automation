"""pipeline-doctor - Diagnose pipeline issues from logs and configs."""

import argparse
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import Any

from skillpack.utils.output import get_output_dir, write_text


def handler(args: argparse.Namespace) -> int:
    """CLI handler for pipeline-doctor."""
    result = pipeline_doctor_main(
        log_path=args.logs,
        config_path=args.config,
        output_dir=args.output_dir,
    )

    if result.get("success"):
        print(f"✅ Diagnosis complete: {result['output_dir']}")
        print(f"   Errors: {result.get('error_count', 0)}")
        print(f"   Warnings: {result.get('warning_count', 0)}")
        return 0
    print(f"❌ Error: {result.get('error')}")
    return 1


def register_parser(subparsers: Any) -> None:
    """Register the pipeline-doctor subcommand."""
    parser = subparsers.add_parser(
        "pipeline-doctor",
        help="Diagnose pipeline issues from logs and configs",
    )
    parser.add_argument(
        "--logs",
        type=Path,
        required=True,
        help="Path to log file or directory",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to pipeline config (optional)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./out/pipeline_doctor"),
        help="Output directory",
    )
    parser.set_defaults(handler=handler)


def pipeline_doctor_main(
    log_path: Path,
    config_path: Path | None = None,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """Diagnose pipeline issues from logs."""
    if output_dir is None:
        output_dir = get_output_dir("pipeline_doctor")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)

    if not log_path.exists():
        return {"success": False, "error": f"Log path not found: {log_path}"}

    try:
        # Collect log files
        if log_path.is_file():
            log_files = [log_path]
        else:
            log_files = list(log_path.rglob("*.log")) + list(log_path.rglob("*.txt"))

        all_issues = []
        error_patterns = []
        timeline = []

        for log_file in log_files:
            content = log_file.read_text(errors="ignore")
            issues = analyze_log(log_file, content)
            all_issues.extend(issues)
            
            patterns = extract_error_patterns(content)
            error_patterns.extend(patterns)
            
            events = extract_timeline(log_file, content)
            timeline.extend(events)

        # Sort timeline
        timeline.sort(key=lambda x: x.get("timestamp", ""))

        # Analyze config if provided
        config_issues = []
        if config_path and config_path.exists():
            config_issues = analyze_config(config_path)
            all_issues.extend(config_issues)

        # Generate diagnosis report
        report = generate_diagnosis_report(all_issues, error_patterns, timeline)
        write_text(content=report, filename="diagnosis.md", skill_name="pipeline_doctor", output_dir=output_dir)

        # Generate remediation suggestions
        remediation = generate_remediation(all_issues, error_patterns)
        write_text(content=remediation, filename="remediation.md", skill_name="pipeline_doctor", output_dir=output_dir)

        error_count = len([i for i in all_issues if i["severity"] == "error"])
        warning_count = len([i for i in all_issues if i["severity"] == "warning"])

        return {
            "success": True,
            "output_dir": str(output_dir),
            "files": ["diagnosis.md", "remediation.md"],
            "error_count": error_count,
            "warning_count": warning_count,
            "log_files_analyzed": len(log_files),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def analyze_log(log_file: Path, content: str) -> list[dict]:
    """Analyze log content for issues."""
    issues = []
    lines = content.split("\n")

    # Error patterns to look for
    patterns = [
        (r"(?i)error[:\s](.+)", "error", "Error detected"),
        (r"(?i)exception[:\s](.+)", "error", "Exception detected"),
        (r"(?i)failed[:\s](.+)", "error", "Failure detected"),
        (r"(?i)traceback", "error", "Python traceback"),
        (r"(?i)warning[:\s](.+)", "warning", "Warning detected"),
        (r"(?i)timeout", "error", "Timeout detected"),
        (r"(?i)out of memory|oom", "error", "Memory issue"),
        (r"(?i)connection refused|connection reset", "error", "Connection issue"),
        (r"(?i)permission denied", "error", "Permission issue"),
        (r"(?i)disk full|no space left", "error", "Disk space issue"),
        (r"(?i)rate limit|throttl", "warning", "Rate limiting"),
        (r"(?i)retry|retrying", "warning", "Retry behavior"),
    ]

    for i, line in enumerate(lines):
        for pattern, severity, description in patterns:
            if re.search(pattern, line):
                issues.append({
                    "file": str(log_file),
                    "line": i + 1,
                    "severity": severity,
                    "description": description,
                    "content": line[:200],
                })
                break

    return issues


def extract_error_patterns(content: str) -> list[dict]:
    """Extract common error patterns."""
    patterns = defaultdict(int)
    
    # Common error types
    error_types = [
        (r"(?:Error|Exception):\s*(\w+(?:Error|Exception))", "exception_type"),
        (r"HTTP\s+(\d{3})", "http_status"),
        (r"exit code[:\s]+(\d+)", "exit_code"),
        (r"(\w+Error):", "error_class"),
    ]

    for pattern, category in error_types:
        for match in re.finditer(pattern, content):
            key = f"{category}:{match.group(1)}"
            patterns[key] += 1

    return [
        {"pattern": k, "count": v, "category": k.split(":")[0]}
        for k, v in sorted(patterns.items(), key=lambda x: -x[1])[:20]
    ]


def extract_timeline(log_file: Path, content: str) -> list[dict]:
    """Extract timeline events from log."""
    events = []
    
    # Common timestamp patterns
    timestamp_patterns = [
        r"(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2})",
        r"(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})",
    ]

    lines = content.split("\n")
    for line in lines[:500]:  # Sample first 500 lines
        for pattern in timestamp_patterns:
            match = re.search(pattern, line)
            if match:
                # Classify event type
                event_type = "info"
                if re.search(r"(?i)error|exception|failed", line):
                    event_type = "error"
                elif re.search(r"(?i)start|begin|init", line):
                    event_type = "start"
                elif re.search(r"(?i)end|complete|finish|success", line):
                    event_type = "end"
                elif re.search(r"(?i)warning", line):
                    event_type = "warning"

                events.append({
                    "timestamp": match.group(1),
                    "type": event_type,
                    "file": str(log_file.name),
                    "content": line[:100],
                })
                break

    return events


def analyze_config(config_path: Path) -> list[dict]:
    """Analyze pipeline config for issues."""
    issues = []
    content = config_path.read_text()

    # Common config issues
    checks = [
        (r"password\s*[=:]\s*\S+", "warning", "Hardcoded password detected"),
        (r"(api_key|secret)\s*[=:]\s*['\"]?\w+", "warning", "Hardcoded secret detected"),
        (r"retry\s*[=:]\s*0", "warning", "Retries disabled"),
        (r"timeout\s*[=:]\s*\d{1,2}(?!\d)", "warning", "Short timeout value"),
        (r"debug\s*[=:]\s*[Tt]rue", "info", "Debug mode enabled"),
    ]

    for pattern, severity, description in checks:
        if re.search(pattern, content):
            issues.append({
                "file": str(config_path),
                "line": 0,
                "severity": severity,
                "description": description,
                "content": "Config check",
            })

    return issues


def generate_diagnosis_report(
    issues: list, patterns: list, timeline: list
) -> str:
    """Generate diagnosis markdown report."""
    
    # Group issues by severity
    errors = [i for i in issues if i["severity"] == "error"]
    warnings = [i for i in issues if i["severity"] == "warning"]

    # Issue table
    error_rows = "\n".join([
        f"| {i['file'].split('/')[-1]} | {i['line']} | {i['description']} |"
        for i in errors[:20]
    ]) or "| No errors found |"

    # Pattern table
    pattern_rows = "\n".join([
        f"| {p['pattern']} | {p['count']} |"
        for p in patterns[:10]
    ]) or "| No patterns found |"

    # Timeline (first/last events)
    first_events = timeline[:5]
    last_events = timeline[-5:] if len(timeline) > 5 else []

    return dedent(f'''\
        # Pipeline Diagnosis Report

        Generated by skillpack pipeline-doctor on {datetime.now().strftime("%Y-%m-%d %H:%M")}

        ## Summary

        | Metric | Value |
        |--------|-------|
        | Errors | {len(errors)} |
        | Warnings | {len(warnings)} |
        | Unique patterns | {len(patterns)} |
        | Timeline events | {len(timeline)} |

        ## Errors Found

        | File | Line | Description |
        |------|------|-------------|
{error_rows}

        ## Error Patterns

        | Pattern | Count |
        |---------|-------|
{pattern_rows}

        ## Timeline

        ### First Events
        {"".join([f"- `{e['timestamp']}` [{e['type']}] {e['content'][:50]}..." + chr(10) for e in first_events]) or "No events"}

        ### Last Events
        {"".join([f"- `{e['timestamp']}` [{e['type']}] {e['content'][:50]}..." + chr(10) for e in last_events]) or "No events"}

        ## Health Indicators

        {"🔴 **Critical**: Multiple errors detected" if len(errors) > 10 else ""}
        {"🟡 **Warning**: Some issues found" if len(warnings) > 5 else ""}
        {"🟢 **Healthy**: Few or no issues" if len(errors) == 0 and len(warnings) < 5 else ""}
    ''')


def generate_remediation(issues: list, patterns: list) -> str:
    """Generate remediation suggestions."""
    
    suggestions = []
    
    # Analyze patterns and suggest fixes
    for pattern in patterns:
        key = pattern["pattern"]
        if "MemoryError" in key or "OOM" in key:
            suggestions.append({
                "issue": "Memory exhaustion",
                "suggestion": "Increase memory limits or optimize batch sizes",
                "priority": "high",
            })
        elif "TimeoutError" in key or "timeout" in key.lower():
            suggestions.append({
                "issue": "Timeouts",
                "suggestion": "Increase timeout values or optimize slow operations",
                "priority": "high",
            })
        elif "ConnectionError" in key or "connection" in key.lower():
            suggestions.append({
                "issue": "Connection failures",
                "suggestion": "Check network connectivity and add retry logic",
                "priority": "high",
            })
        elif "HTTP:5" in key:
            suggestions.append({
                "issue": "Server errors (5xx)",
                "suggestion": "Check downstream service health",
                "priority": "high",
            })
        elif "HTTP:4" in key:
            suggestions.append({
                "issue": "Client errors (4xx)",
                "suggestion": "Validate request payloads and authentication",
                "priority": "medium",
            })

    # Deduplicate
    seen = set()
    unique_suggestions = []
    for s in suggestions:
        if s["issue"] not in seen:
            seen.add(s["issue"])
            unique_suggestions.append(s)

    suggestion_rows = "\n".join([
        f"| {s['issue']} | {s['suggestion']} | {s['priority']} |"
        for s in unique_suggestions
    ]) or "| No specific suggestions |"

    return dedent(f'''\
        # Remediation Suggestions

        Generated by skillpack pipeline-doctor on {datetime.now().strftime("%Y-%m-%d %H:%M")}

        ## Recommended Actions

        | Issue | Suggestion | Priority |
        |-------|------------|----------|
{suggestion_rows}

        ## General Best Practices

        ### Error Handling
        - Implement exponential backoff for retries
        - Add circuit breakers for external dependencies
        - Log structured errors with context

        ### Monitoring
        - Set up alerts for error rate thresholds
        - Monitor memory and CPU usage
        - Track pipeline latency percentiles

        ### Recovery
        - Implement checkpointing for long-running jobs
        - Design for idempotent operations
        - Maintain dead-letter queues for failed records
    ''')
