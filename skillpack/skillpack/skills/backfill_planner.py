"""backfill-planner - Generate backfill plans with date ranges and checkpoints."""

import argparse
from datetime import datetime, timedelta
from pathlib import Path
from textwrap import dedent
from typing import Any

from skillpack.utils.output import get_output_dir, write_text


def handler(args: argparse.Namespace) -> int:
    """CLI handler for backfill-planner."""
    result = backfill_planner_main(
        pipeline_name=args.name,
        start_date=args.start_date,
        end_date=args.end_date,
        partition_by=args.partition_by,
        batch_size=args.batch_size,
        output_dir=args.output_dir,
    )

    if result.get("success"):
        print(f"✅ Generated backfill plan: {result['plan_file']}")
        return 0
    print(f"❌ Error: {result.get('error')}")
    return 1


def register_parser(subparsers: Any) -> None:
    """Register the backfill-planner subcommand."""
    parser = subparsers.add_parser(
        "backfill-planner",
        help="Generate backfill plans with date ranges and checkpoints",
    )
    parser.add_argument("--name", required=True, help="Pipeline name")
    parser.add_argument("--start-date", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument(
        "--partition-by",
        choices=["day", "week", "month"],
        default="day",
        help="Partition granularity",
    )
    parser.add_argument(
        "--batch-size", type=int, default=7, help="Batch size for parallel runs"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./out/backfill_planner"),
        help="Output directory",
    )
    parser.set_defaults(handler=handler)


def backfill_planner_main(
    pipeline_name: str,
    start_date: str,
    end_date: str,
    partition_by: str = "day",
    batch_size: int = 7,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """Generate a backfill plan with date ranges and checkpoints."""
    if output_dir is None:
        output_dir = get_output_dir("backfill_planner")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        partitions = generate_partitions(start, end, partition_by)
        batches = create_batches(partitions, batch_size)

        # Generate plan markdown
        plan_md = generate_plan_md(pipeline_name, partitions, batches, start_date, end_date)
        plan_file = write_text(
            content=plan_md, filename="backfill_plan.md", skill_name="backfill_planner"
        )

        # Generate runner script
        runner = generate_runner_script(pipeline_name, partitions, batches)
        write_text(content=runner, filename="backfill.py", skill_name="backfill_planner")

        # Generate checkpoint file
        checkpoint = generate_checkpoint_template(partitions)
        write_text(
            content=checkpoint, filename="checkpoint.json", skill_name="backfill_planner"
        )

        return {
            "success": True,
            "plan_file": str(plan_file),
            "total_partitions": len(partitions),
            "total_batches": len(batches),
            "output_dir": str(output_dir),
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_partitions(start: datetime, end: datetime, partition_by: str) -> list[dict]:
    """Generate partition list based on granularity."""
    partitions = []
    current = start

    if partition_by == "day":
        delta = timedelta(days=1)
    elif partition_by == "week":
        delta = timedelta(weeks=1)
    elif partition_by == "month":
        delta = timedelta(days=30)
    else:
        delta = timedelta(days=1)

    idx = 0
    while current <= end:
        partitions.append({
            "id": idx,
            "start": current.strftime("%Y-%m-%d"),
            "end": (current + delta - timedelta(days=1)).strftime("%Y-%m-%d"),
            "status": "pending",
        })
        current += delta
        idx += 1

    return partitions


def create_batches(partitions: list[dict], batch_size: int) -> list[list[dict]]:
    """Group partitions into batches."""
    return [partitions[i : i + batch_size] for i in range(0, len(partitions), batch_size)]


def generate_plan_md(
    pipeline_name: str,
    partitions: list[dict],
    batches: list[list[dict]],
    start_date: str,
    end_date: str,
) -> str:
    """Generate markdown backfill plan."""
    partition_table = "\n".join(
        [f"| {p['id']:3} | {p['start']} | {p['end']} | {p['status']} |" for p in partitions]
    )

    return dedent(f'''\
        # Backfill Plan: {pipeline_name}

        ## Summary
        - **Date Range**: {start_date} to {end_date}
        - **Total Partitions**: {len(partitions)}
        - **Total Batches**: {len(batches)}
        - **Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

        ## Partitions
        | ID  | Start Date | End Date   | Status  |
        |-----|------------|------------|---------|
{partition_table}

        ## Execution Plan
        
        Run batches sequentially to avoid resource contention:
        
        ```bash
        python backfill.py --batch 0  # Partitions 0-{min(len(partitions)-1, 6)}
        python backfill.py --batch 1  # Partitions 7-{min(len(partitions)-1, 13)}
        # ... continue for all batches
        ```

        ## Checkpointing
        - Checkpoint file: `checkpoint.json`
        - Resume from last successful partition
        - Idempotent: safe to re-run failed partitions

        ## Rollback
        1. Identify failed partitions in checkpoint.json
        2. Delete partial data for those partitions
        3. Re-run from checkpoint
    ''')


def generate_runner_script(
    pipeline_name: str, partitions: list[dict], batches: list[list[dict]]
) -> str:
    """Generate Python runner script."""
    return dedent(f'''\
        #!/usr/bin/env python3
        """Backfill runner for {pipeline_name}."""

        import argparse
        import json
        import sys
        from datetime import datetime
        from pathlib import Path


        CHECKPOINT_FILE = Path("checkpoint.json")
        PARTITIONS = {partitions}


        def load_checkpoint() -> dict:
            if CHECKPOINT_FILE.exists():
                return json.loads(CHECKPOINT_FILE.read_text())
            return {{"completed": [], "failed": []}}


        def save_checkpoint(checkpoint: dict) -> None:
            CHECKPOINT_FILE.write_text(json.dumps(checkpoint, indent=2))


        def run_partition(partition: dict) -> bool:
            \"\"\"Run a single partition. Returns True on success.\"\"\"
            print(f"Running partition {{partition['id']}}: {{partition['start']}} to {{partition['end']}}")
            
            # TODO: Implement your pipeline logic here
            # Example:
            # subprocess.run(["python", "pipeline.py", "--date", partition["start"]])
            
            return True  # Return False on failure


        def main() -> int:
            parser = argparse.ArgumentParser(description="Backfill runner")
            parser.add_argument("--batch", type=int, help="Run specific batch")
            parser.add_argument("--partition", type=int, help="Run specific partition")
            parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
            args = parser.parse_args()

            checkpoint = load_checkpoint()
            completed = set(checkpoint.get("completed", []))

            partitions_to_run = PARTITIONS
            if args.partition is not None:
                partitions_to_run = [p for p in PARTITIONS if p["id"] == args.partition]
            elif args.batch is not None:
                batch_size = 7
                start_idx = args.batch * batch_size
                partitions_to_run = PARTITIONS[start_idx : start_idx + batch_size]

            for partition in partitions_to_run:
                if args.resume and partition["id"] in completed:
                    print(f"Skipping completed partition {{partition['id']}}")
                    continue

                success = run_partition(partition)
                if success:
                    checkpoint["completed"].append(partition["id"])
                else:
                    checkpoint["failed"].append(partition["id"])
                save_checkpoint(checkpoint)

            print(f"Completed: {{len(checkpoint['completed'])}}/{{len(PARTITIONS)}}")
            return 0


        if __name__ == "__main__":
            sys.exit(main())
    ''')


def generate_checkpoint_template(partitions: list[dict]) -> str:
    """Generate checkpoint JSON template."""
    import json

    return json.dumps(
        {
            "pipeline": "backfill",
            "total_partitions": len(partitions),
            "completed": [],
            "failed": [],
            "last_updated": datetime.now().isoformat(),
        },
        indent=2,
    )
