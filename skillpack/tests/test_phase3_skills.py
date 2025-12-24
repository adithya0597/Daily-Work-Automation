"""Tests for Phase 3 ML skills."""

import tempfile
from pathlib import Path

import pytest


class TestBaselineModelFactory:
    """Tests for baseline-model-factory skill."""

    def test_baseline_model_factory_classification(self):
        """Test generating classification baseline."""
        from skillpack.skills.baseline_model_factory import baseline_model_factory_main

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            result = baseline_model_factory_main(
                model_name="test_classifier",
                task_type="classification",
                output_dir=output_dir,
            )

            assert result["success"] is True


class TestFeatureEngineering:
    """Tests for feature-engineering skill."""

    def test_feature_engineering_main(self):
        """Test generating feature transformers."""
        from skillpack.skills.feature_engineering import feature_engineering_main

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            result = feature_engineering_main(
                columns=[  # Correct param name (not config)
                    {"name": "age", "type": "numeric"},
                    {"name": "date", "type": "datetime"},
                ],
                output_dir=output_dir,
            )

            assert result["success"] is True


class TestHyperparameterSearch:
    """Tests for hyperparameter-search skill."""

    def test_hyperparameter_search_optuna(self):
        """Test generating Optuna sweep."""
        from skillpack.skills.hyperparameter_search import hyperparameter_search_main

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            result = hyperparameter_search_main(
                experiment_name="test_sweep",
                framework="optuna",
                model_type="sklearn",
                output_dir=output_dir,
            )

            assert result["success"] is True


class TestExperimentTracking:
    """Tests for experiment-tracking skill."""

    def test_experiment_tracking_mlflow(self):
        """Test generating MLflow tracker."""
        from skillpack.skills.experiment_tracking import experiment_tracking_main

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            result = experiment_tracking_main(
                project_name="test_project",
                tracker="mlflow",
                output_dir=output_dir,
            )

            assert result["success"] is True


class TestEvaluationReport:
    """Tests for evaluation-report skill."""

    def test_evaluation_report_classification(self):
        """Test generating classification eval report."""
        from skillpack.skills.evaluation_report import evaluation_report_main

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            result = evaluation_report_main(
                model_name="test_model",
                task_type="classification",
                output_dir=output_dir,
            )

            assert result["success"] is True


class TestExperimentQueue:
    """Tests for experiment-queue skill."""

    def test_experiment_queue_main(self):
        """Test generating experiment queue."""
        from skillpack.skills.experiment_queue import experiment_queue_main

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            result = experiment_queue_main(
                queue_name="test_queue",
                output_dir=output_dir,
            )

            assert result["success"] is True
