"""evaluation-report - Generate model evaluation reports with metrics and plots."""

import argparse
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import Any

import yaml

from skillpack.utils.output import get_output_dir, write_text


def handler(args: argparse.Namespace) -> int:
    """CLI handler for evaluation-report."""
    # Load metrics if provided
    metrics = {}
    if args.metrics and args.metrics.exists():
        with open(args.metrics) as f:
            metrics = yaml.safe_load(f) or {}

    result = evaluation_report_main(
        model_name=args.name,
        task_type=args.task,
        metrics=metrics,
        output_dir=args.output_dir,
    )

    if result.get("success"):
        print(f"✅ Generated evaluation report: {result['output_dir']}")
        return 0
    print(f"❌ Error: {result.get('error')}")
    return 1


def register_parser(subparsers: Any) -> None:
    """Register the evaluation-report subcommand."""
    parser = subparsers.add_parser(
        "evaluation-report",
        help="Generate model evaluation reports with metrics and plots",
    )
    parser.add_argument("--name", required=True, help="Model name")
    parser.add_argument(
        "--task",
        choices=["classification", "regression"],
        default="classification",
        help="Task type",
    )
    parser.add_argument(
        "--metrics",
        type=Path,
        help="Path to metrics YAML file",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./out/evaluation_report"),
        help="Output directory",
    )
    parser.set_defaults(handler=handler)


def evaluation_report_main(
    model_name: str,
    task_type: str = "classification",
    metrics: dict | None = None,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """Generate model evaluation report."""
    if output_dir is None:
        output_dir = get_output_dir("evaluation_report")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)

    if metrics is None:
        metrics = generate_sample_metrics(task_type)

    try:
        files = []

        # Generate report markdown
        report = generate_report(model_name, task_type, metrics)
        write_text(content=report, filename="evaluation_report.md", skill_name="evaluation_report")
        files.append("evaluation_report.md")

        # Generate evaluation script
        eval_script = generate_eval_script(model_name, task_type)
        write_text(content=eval_script, filename="evaluate.py", skill_name="evaluation_report")
        files.append("evaluate.py")

        # Generate plotting script
        plot_script = generate_plot_script(task_type)
        write_text(content=plot_script, filename="plot_results.py", skill_name="evaluation_report")
        files.append("plot_results.py")

        # Save metrics as YAML
        write_text(
            content=yaml.dump(metrics, default_flow_style=False),
            filename="metrics.yaml",
            skill_name="evaluation_report",
        )
        files.append("metrics.yaml")

        return {
            "success": True,
            "output_dir": str(output_dir),
            "files": files,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_sample_metrics(task_type: str) -> dict:
    """Generate sample metrics."""
    if task_type == "classification":
        return {
            "accuracy": 0.92,
            "precision": 0.91,
            "recall": 0.93,
            "f1": 0.92,
            "auc_roc": 0.96,
            "confusion_matrix": [[850, 50], [30, 70]],
            "class_report": {
                "0": {"precision": 0.97, "recall": 0.94, "f1": 0.95},
                "1": {"precision": 0.58, "recall": 0.70, "f1": 0.64},
            },
        }
    else:
        return {
            "mse": 0.0234,
            "rmse": 0.153,
            "mae": 0.112,
            "r2": 0.89,
            "mape": 5.2,
            "residual_mean": 0.002,
            "residual_std": 0.15,
        }


def generate_report(model_name: str, task_type: str, metrics: dict) -> str:
    """Generate evaluation report markdown."""
    
    if task_type == "classification":
        metrics_table = f"""
| Metric | Value |
|--------|-------|
| Accuracy | {metrics.get('accuracy', 0):.4f} |
| Precision | {metrics.get('precision', 0):.4f} |
| Recall | {metrics.get('recall', 0):.4f} |
| F1 Score | {metrics.get('f1', 0):.4f} |
| AUC-ROC | {metrics.get('auc_roc', 0):.4f} |
"""
        analysis = """
## Analysis

### Performance Summary
- Model achieves strong overall accuracy
- Check class imbalance if precision/recall differ significantly
- AUC-ROC indicates good discrimination ability

### Potential Issues
- [ ] Class imbalance (check confusion matrix)
- [ ] Overfitting (compare train vs test metrics)
- [ ] Calibration (if using probabilities)
"""
    else:
        metrics_table = f"""
| Metric | Value |
|--------|-------|
| MSE | {metrics.get('mse', 0):.6f} |
| RMSE | {metrics.get('rmse', 0):.4f} |
| MAE | {metrics.get('mae', 0):.4f} |
| R² | {metrics.get('r2', 0):.4f} |
| MAPE | {metrics.get('mape', 0):.2f}% |
"""
        analysis = """
## Analysis

### Performance Summary
- R² indicates variance explained by the model
- MAPE shows average percentage error
- Check residual distribution for homoscedasticity

### Potential Issues
- [ ] Heteroscedastic residuals
- [ ] Non-linear patterns in residuals
- [ ] Outlier sensitivity
"""

    return dedent(f'''\
        # Model Evaluation Report: {model_name}

        **Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M")}  
        **Task Type**: {task_type.title()}

        ---

        ## Metrics Summary

{metrics_table}

{analysis}

        ## Recommendations

        ### Short-term
        1. Review confusion matrix / residual plots
        2. Check feature importance
        3. Validate on holdout set

        ### Long-term
        1. Set up monitoring for metric drift
        2. A/B test before full deployment
        3. Document model limitations

        ## Next Steps

        - [ ] Generate detailed plots: `python plot_results.py`
        - [ ] Compare with baseline model
        - [ ] Review with stakeholders
    ''')


def generate_eval_script(model_name: str, task_type: str) -> str:
    """Generate evaluation script."""
    
    if task_type == "classification":
        metrics_code = """
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

def calculate_metrics(y_true, y_pred, y_prob=None):
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average="weighted"),
        "recall": recall_score(y_true, y_pred, average="weighted"),
        "f1": f1_score(y_true, y_pred, average="weighted"),
    }
    
    if y_prob is not None:
        metrics["auc_roc"] = roc_auc_score(y_true, y_prob)
    
    metrics["confusion_matrix"] = confusion_matrix(y_true, y_pred).tolist()
    metrics["class_report"] = classification_report(y_true, y_pred, output_dict=True)
    
    return metrics
"""
    else:
        metrics_code = """
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

def calculate_metrics(y_true, y_pred):
    residuals = y_true - y_pred
    
    metrics = {
        "mse": mean_squared_error(y_true, y_pred),
        "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
        "mae": mean_absolute_error(y_true, y_pred),
        "r2": r2_score(y_true, y_pred),
        "mape": np.mean(np.abs((y_true - y_pred) / y_true)) * 100,
        "residual_mean": float(np.mean(residuals)),
        "residual_std": float(np.std(residuals)),
    }
    
    return metrics
"""

    return dedent(f'''\
        #!/usr/bin/env python3
        """Evaluation script for {model_name}.

        Generated by skillpack on {datetime.now().strftime("%Y-%m-%d %H:%M")}
        """

        import argparse
        from pathlib import Path

        import joblib
        import pandas as pd
        import yaml

{metrics_code}


        def main():
            parser = argparse.ArgumentParser()
            parser.add_argument("--model", type=Path, required=True)
            parser.add_argument("--data", type=Path, required=True)
            parser.add_argument("--target", default="target")
            parser.add_argument("--output", type=Path, default=Path("metrics.yaml"))
            args = parser.parse_args()
            
            # Load model and data
            model = joblib.load(args.model)
            df = pd.read_csv(args.data)
            
            X = df.drop(columns=[args.target])
            y_true = df[args.target]
            
            # Predict
            y_pred = model.predict(X)
            {"y_prob = model.predict_proba(X)[:, 1] if hasattr(model, 'predict_proba') else None" if task_type == "classification" else ""}
            
            # Calculate metrics
            metrics = calculate_metrics(y_true, y_pred{"" if task_type == "regression" else ", y_prob"})
            
            # Save
            with open(args.output, "w") as f:
                yaml.dump(metrics, f)
            
            print(f"Metrics saved to {{args.output}}")


        if __name__ == "__main__":
            main()
    ''')


def generate_plot_script(task_type: str) -> str:
    """Generate plotting script."""
    
    if task_type == "classification":
        plots = """
def plot_confusion_matrix(cm, output_path):
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.savefig(output_path / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close()


def plot_roc_curve(y_true, y_prob, output_path):
    from sklearn.metrics import roc_curve, auc
    
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f"ROC (AUC = {roc_auc:.3f})")
    plt.plot([0, 1], [0, 1], "k--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend()
    plt.savefig(output_path / "roc_curve.png", dpi=150, bbox_inches="tight")
    plt.close()
"""
    else:
        plots = """
def plot_residuals(y_true, y_pred, output_path):
    residuals = y_true - y_pred
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Residual distribution
    axes[0].hist(residuals, bins=50, edgecolor="black")
    axes[0].set_xlabel("Residual")
    axes[0].set_title("Residual Distribution")
    
    # Residual vs Predicted
    axes[1].scatter(y_pred, residuals, alpha=0.5)
    axes[1].axhline(y=0, color="r", linestyle="--")
    axes[1].set_xlabel("Predicted")
    axes[1].set_ylabel("Residual")
    axes[1].set_title("Residuals vs Predicted")
    
    plt.tight_layout()
    plt.savefig(output_path / "residuals.png", dpi=150, bbox_inches="tight")
    plt.close()


def plot_actual_vs_predicted(y_true, y_pred, output_path):
    plt.figure(figsize=(8, 8))
    plt.scatter(y_true, y_pred, alpha=0.5)
    
    # Perfect prediction line
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], "r--")
    
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title("Actual vs Predicted")
    plt.savefig(output_path / "actual_vs_predicted.png", dpi=150, bbox_inches="tight")
    plt.close()
"""

    return dedent(f'''\
        #!/usr/bin/env python3
        """Plotting script for evaluation results.

        Generated by skillpack on {datetime.now().strftime("%Y-%m-%d %H:%M")}
        """

        import argparse
        from pathlib import Path

        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np

        sns.set_style("whitegrid")

{plots}


        def main():
            parser = argparse.ArgumentParser()
            parser.add_argument("--output", type=Path, default=Path("./plots"))
            args = parser.parse_args()
            
            args.output.mkdir(exist_ok=True)
            
            # TODO: Load your actual data
            # y_true, y_pred = load_predictions()
            
            print(f"Plots saved to {{args.output}}")


        if __name__ == "__main__":
            main()
    ''')
