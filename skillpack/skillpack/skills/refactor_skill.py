"""refactor-skill - Identify complexity hotspots and propose safe refactors."""

import argparse
import ast
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import Any

from skillpack.utils.output import get_output_dir, write_text


def handler(args: argparse.Namespace) -> int:
    """CLI handler for refactor-skill."""
    result = refactor_skill_main(
        source_path=args.source,
        threshold=args.threshold,
        output_dir=args.output_dir,
    )

    if result.get("success"):
        print(f"✅ Analysis complete: {result['output_dir']}")
        print(f"   Hotspots found: {result.get('hotspot_count', 0)}")
        print(f"   Suggestions: {result.get('suggestion_count', 0)}")
        return 0
    print(f"❌ Error: {result.get('error')}")
    return 1


def register_parser(subparsers: Any) -> None:
    """Register the refactor-skill subcommand."""
    parser = subparsers.add_parser(
        "refactor-skill",
        help="Identify complexity hotspots and propose safe refactors",
    )
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Path to Python source file or directory",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=10,
        help="Complexity threshold for flagging (default: 10)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./out/refactor_skill"),
        help="Output directory",
    )
    parser.set_defaults(handler=handler)


def refactor_skill_main(
    source_path: Path,
    threshold: int = 10,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """Analyze code for complexity and suggest refactorings."""
    if output_dir is None:
        output_dir = get_output_dir("refactor_skill")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)

    if not source_path.exists():
        return {"success": False, "error": f"Path not found: {source_path}"}

    try:
        # Collect files
        if source_path.is_file():
            files = [source_path]
        else:
            files = list(source_path.rglob("*.py"))

        all_hotspots = []
        all_suggestions = []
        file_metrics = []

        for file_path in files:
            try:
                source = file_path.read_text()
                tree = ast.parse(source)

                # Analyze file
                metrics = analyze_file(file_path, tree, source)
                file_metrics.append(metrics)

                # Find hotspots
                hotspots = find_hotspots(file_path, tree, source, threshold)
                all_hotspots.extend(hotspots)

                # Generate suggestions
                suggestions = generate_suggestions(file_path, tree, source, hotspots)
                all_suggestions.extend(suggestions)

            except SyntaxError:
                continue

        # Generate report
        report = generate_report(file_metrics, all_hotspots, all_suggestions, threshold)
        write_text(content=report, filename="refactor_report.md", skill_name="refactor_skill")

        # Generate metrics JSON
        metrics_json = generate_metrics_json(file_metrics, all_hotspots)
        write_text(content=metrics_json, filename="metrics.json", skill_name="refactor_skill")

        return {
            "success": True,
            "output_dir": str(output_dir),
            "files": ["refactor_report.md", "metrics.json"],
            "hotspot_count": len(all_hotspots),
            "suggestion_count": len(all_suggestions),
            "files_analyzed": len(files),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def analyze_file(file_path: Path, tree: ast.AST, source: str) -> dict:
    """Analyze a file for complexity metrics."""
    lines = source.split("\n")
    
    functions = []
    classes = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            complexity = calculate_cyclomatic_complexity(node)
            loc = node.end_lineno - node.lineno + 1 if node.end_lineno else 0
            functions.append({
                "name": node.name,
                "line": node.lineno,
                "complexity": complexity,
                "loc": loc,
                "args": len(node.args.args),
            })
        elif isinstance(node, ast.ClassDef):
            method_count = sum(1 for n in node.body if isinstance(n, ast.FunctionDef))
            classes.append({
                "name": node.name,
                "line": node.lineno,
                "methods": method_count,
            })

    return {
        "file": str(file_path),
        "total_lines": len(lines),
        "code_lines": len([l for l in lines if l.strip() and not l.strip().startswith("#")]),
        "functions": functions,
        "classes": classes,
        "avg_complexity": sum(f["complexity"] for f in functions) / len(functions) if functions else 0,
    }


def calculate_cyclomatic_complexity(node: ast.FunctionDef) -> int:
    """Calculate cyclomatic complexity of a function."""
    complexity = 1  # Base complexity
    
    for child in ast.walk(node):
        # Decision points
        if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
            complexity += 1
        elif isinstance(child, ast.BoolOp):
            complexity += len(child.values) - 1
        elif isinstance(child, ast.comprehension):
            complexity += 1 + len(child.ifs)
        elif isinstance(child, ast.Match):
            complexity += len(child.cases)
    
    return complexity


def find_hotspots(
    file_path: Path, tree: ast.AST, source: str, threshold: int
) -> list[dict]:
    """Find complexity hotspots in code."""
    hotspots = []
    lines = source.split("\n")
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            complexity = calculate_cyclomatic_complexity(node)
            loc = node.end_lineno - node.lineno + 1 if node.end_lineno else 0
            args_count = len(node.args.args)
            
            issues = []
            
            if complexity > threshold:
                issues.append(f"High complexity: {complexity} (threshold: {threshold})")
            
            if loc > 50:
                issues.append(f"Long function: {loc} lines")
            
            if args_count > 5:
                issues.append(f"Too many arguments: {args_count}")
            
            # Check for nested functions
            nested = sum(1 for n in ast.walk(node) if isinstance(n, ast.FunctionDef)) - 1
            if nested > 0:
                issues.append(f"Nested functions: {nested}")
            
            # Check for deep nesting
            max_depth = calculate_nesting_depth(node)
            if max_depth > 4:
                issues.append(f"Deep nesting: {max_depth} levels")
            
            if issues:
                hotspots.append({
                    "file": str(file_path),
                    "function": node.name,
                    "line": node.lineno,
                    "complexity": complexity,
                    "loc": loc,
                    "issues": issues,
                })
    
    return hotspots


def calculate_nesting_depth(node: ast.AST, depth: int = 0) -> int:
    """Calculate maximum nesting depth."""
    max_depth = depth
    
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
            child_depth = calculate_nesting_depth(child, depth + 1)
            max_depth = max(max_depth, child_depth)
        else:
            child_depth = calculate_nesting_depth(child, depth)
            max_depth = max(max_depth, child_depth)
    
    return max_depth


def generate_suggestions(
    file_path: Path, tree: ast.AST, source: str, hotspots: list
) -> list[dict]:
    """Generate refactoring suggestions."""
    suggestions = []
    
    for hotspot in hotspots:
        func_name = hotspot["function"]
        
        for issue in hotspot["issues"]:
            if "High complexity" in issue:
                suggestions.append({
                    "file": str(file_path),
                    "function": func_name,
                    "line": hotspot["line"],
                    "type": "extract_method",
                    "description": f"Extract conditional branches into separate methods",
                    "priority": "high",
                })
            
            if "Long function" in issue:
                suggestions.append({
                    "file": str(file_path),
                    "function": func_name,
                    "line": hotspot["line"],
                    "type": "split_function",
                    "description": "Split into smaller, focused functions",
                    "priority": "high",
                })
            
            if "Too many arguments" in issue:
                suggestions.append({
                    "file": str(file_path),
                    "function": func_name,
                    "line": hotspot["line"],
                    "type": "introduce_parameter_object",
                    "description": "Group related parameters into a dataclass",
                    "priority": "medium",
                })
            
            if "Deep nesting" in issue:
                suggestions.append({
                    "file": str(file_path),
                    "function": func_name,
                    "line": hotspot["line"],
                    "type": "guard_clauses",
                    "description": "Use early returns/guard clauses to reduce nesting",
                    "priority": "medium",
                })
    
    return suggestions


def generate_report(
    file_metrics: list, hotspots: list, suggestions: list, threshold: int
) -> str:
    """Generate markdown report."""
    
    # Summary stats
    total_functions = sum(len(m["functions"]) for m in file_metrics)
    total_lines = sum(m["total_lines"] for m in file_metrics)
    high_complexity = len([h for h in hotspots if h["complexity"] > threshold])
    
    # Hotspot table
    hotspot_rows = []
    for h in sorted(hotspots, key=lambda x: x["complexity"], reverse=True)[:10]:
        hotspot_rows.append(
            f"| {Path(h['file']).name} | {h['function']} | {h['line']} | {h['complexity']} | {h['loc']} |"
        )
    hotspot_table = "\n".join(hotspot_rows) if hotspot_rows else "| No hotspots found |"
    
    # Suggestions grouped by type
    suggestions_by_type = defaultdict(list)
    for s in suggestions:
        suggestions_by_type[s["type"]].append(s)
    
    suggestion_sections = []
    for stype, items in suggestions_by_type.items():
        section = f"### {stype.replace('_', ' ').title()}\n"
        for item in items[:5]:
            section += f"- `{item['function']}` ({Path(item['file']).name}:{item['line']}): {item['description']}\n"
        suggestion_sections.append(section)
    
    suggestions_md = "\n".join(suggestion_sections) if suggestion_sections else "No suggestions."
    
    return dedent(f'''\
        # Refactoring Report

        Generated by skillpack refactor-skill on {datetime.now().strftime("%Y-%m-%d %H:%M")}

        ## Summary

        | Metric | Value |
        |--------|-------|
        | Files analyzed | {len(file_metrics)} |
        | Total functions | {total_functions} |
        | Total lines | {total_lines} |
        | Complexity threshold | {threshold} |
        | Hotspots found | {len(hotspots)} |
        | High complexity | {high_complexity} |

        ## Top Complexity Hotspots

        | File | Function | Line | Complexity | LOC |
        |------|----------|------|------------|-----|
{hotspot_table}

        ## Refactoring Suggestions

{suggestions_md}

        ## Best Practices

        ### Reducing Complexity
        1. **Extract Method**: Move complex conditionals into well-named methods
        2. **Guard Clauses**: Use early returns to flatten nested conditions
        3. **Strategy Pattern**: Replace complex switch/if chains with polymorphism

        ### Function Design
        1. Keep functions under 50 lines
        2. Limit to 3-4 parameters (use dataclasses for more)
        3. Single responsibility: one function, one purpose
    ''')


def generate_metrics_json(file_metrics: list, hotspots: list) -> str:
    """Generate metrics as JSON."""
    import json
    
    return json.dumps({
        "generated": datetime.now().isoformat(),
        "files": file_metrics,
        "hotspots": hotspots,
        "summary": {
            "total_files": len(file_metrics),
            "total_hotspots": len(hotspots),
            "total_functions": sum(len(m["functions"]) for m in file_metrics),
        },
    }, indent=2)
