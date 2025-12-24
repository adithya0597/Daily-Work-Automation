"""Tests for Phase 4 infrastructure/serving skills."""

import tempfile
from pathlib import Path

import pytest


class TestFastapiServing:
    """Tests for fastapi-serving skill."""

    def test_fastapi_serving_main(self):
        """Test generating FastAPI service."""
        from skillpack.skills.fastapi_serving import fastapi_serving_main

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            result = fastapi_serving_main(
                model_name="test_api",  # Correct param (not service_name)
                model_type="sklearn",
                output_dir=output_dir,
            )

            assert result["success"] is True


class TestContainerization:
    """Tests for containerization skill."""

    def test_containerization_python(self):
        """Test generating Python Dockerfile."""
        from skillpack.skills.containerization import containerization_main

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            result = containerization_main(
                service_name="test_service",
                base_image="python",
                runtime="uvicorn",  # Correct runtime
                port=8000,
                output_dir=output_dir,
            )

            assert result["success"] is True


class TestIacBoilerplate:
    """Tests for iac-boilerplate skill."""

    def test_iac_boilerplate_aws(self):
        """Test generating AWS Terraform."""
        from skillpack.skills.iac_boilerplate import iac_boilerplate_main

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            result = iac_boilerplate_main(
                project_name="test_infra",
                cloud="aws",
                resources=["compute", "storage"],
                output_dir=output_dir,
            )

            assert result["success"] is True


class TestMonitoringDrift:
    """Tests for monitoring-drift skill."""

    def test_monitoring_drift_main(self):
        """Test generating drift monitors."""
        from skillpack.skills.monitoring_drift import monitoring_drift_main

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            result = monitoring_drift_main(
                model_name="test_model",
                drift_type="both",
                output_dir=output_dir,
            )

            assert result["success"] is True


class TestCostRegression:
    """Tests for cost-regression skill."""

    def test_cost_regression_main(self):
        """Test generating cost analyzer."""
        from skillpack.skills.cost_regression import cost_regression_main

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            result = cost_regression_main(
                project_name="test_project",
                threshold=0.1,
                output_dir=output_dir,
            )

            assert result["success"] is True
