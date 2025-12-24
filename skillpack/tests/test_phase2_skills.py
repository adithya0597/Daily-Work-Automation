"""Tests for Phase 2 ETL/orchestration skills."""

import tempfile
from pathlib import Path

import pytest


class TestDagAuthoring:
    """Tests for dag-authoring skill."""

    def test_dag_authoring_airflow(self):
        """Test generating Airflow DAG."""
        from skillpack.skills.dag_authoring import dag_authoring_main

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            result = dag_authoring_main(
                dag_name="test_pipeline",  # Correct param
                framework="airflow",
                schedule="@daily",
                output_dir=output_dir,
            )

            assert result["success"] is True

    def test_dag_authoring_prefect(self):
        """Test generating Prefect flow."""
        from skillpack.skills.dag_authoring import dag_authoring_main

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            result = dag_authoring_main(
                dag_name="test_flow",
                framework="prefect",
                output_dir=output_dir,
            )

            assert result["success"] is True


class TestBackfillPlanner:
    """Tests for backfill-planner skill."""

    def test_backfill_planner_main(self):
        """Test generating backfill plan."""
        from skillpack.skills.backfill_planner import backfill_planner_main

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            result = backfill_planner_main(
                pipeline_name="test_pipeline",
                start_date="2024-01-01",
                end_date="2024-01-31",
                partition_by="day",
                batch_size=7,
                output_dir=output_dir,
            )

            assert result["success"] is True
            assert result["total_partitions"] == 31


class TestPipelineDoctor:
    """Tests for pipeline-doctor skill."""

    def test_pipeline_doctor_main(self):
        """Test diagnosing pipeline from logs."""
        from skillpack.skills.pipeline_doctor import pipeline_doctor_main

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a log file with errors
            log_path = Path(tmpdir) / "pipeline.log"
            log_path.write_text("""
2024-01-15 10:00:00 INFO Starting pipeline
2024-01-15 10:05:00 ERROR Connection refused to database
2024-01-15 10:05:01 WARNING Retry attempt 1
2024-01-15 10:10:00 ERROR TimeoutError: Query took too long
2024-01-15 10:15:00 INFO Pipeline completed with errors
""")

            output_dir = Path(tmpdir) / "output"
            result = pipeline_doctor_main(
                log_path=log_path,  # Correct param
                output_dir=output_dir,
            )

            assert result["success"] is True
            assert result["error_count"] >= 2


class TestDailyOpsSummary:
    """Tests for daily-ops-summary skill."""

    def test_daily_ops_summary_main(self):
        """Test generating daily ops summary."""
        from skillpack.skills.daily_ops_summary import daily_ops_summary_main

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            result = daily_ops_summary_main(
                date="2024-01-15",
                team="Data Platform",
                output_dir=output_dir,
            )

            assert result["success"] is True
