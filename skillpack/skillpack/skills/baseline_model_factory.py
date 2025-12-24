"""baseline-model-factory - Build scikit-learn baselines with proper pipelines and config."""

import argparse
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import Any

import yaml

from skillpack.utils.output import get_output_dir, write_text


def handler(args: argparse.Namespace) -> int:
    """CLI handler for baseline-model-factory."""
    # Load config if provided
    config = {}
    if args.config and args.config.exists():
        with open(args.config) as f:
            config = yaml.safe_load(f) or {}

    result = baseline_model_factory_main(
        model_name=args.name,
        task_type=args.task,
        features=config.get("features", []),
        target=config.get("target", "target"),
        output_dir=args.output_dir,
    )

    if result.get("success"):
        print(f"✅ Generated baseline model: {result['output_dir']}")
        for f in result.get("files", []):
            print(f"   - {f}")
        return 0
    print(f"❌ Error: {result.get('error')}")
    return 1


def register_parser(subparsers: Any) -> None:
    """Register the baseline-model-factory subcommand."""
    parser = subparsers.add_parser(
        "baseline-model-factory",
        help="Build scikit-learn baselines with proper pipelines and config",
    )
    parser.add_argument("--name", required=True, help="Model name")
    parser.add_argument(
        "--task",
        choices=["classification", "regression"],
        default="classification",
        help="ML task type",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to model configuration YAML",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./out/baseline_model_factory"),
        help="Output directory",
    )
    parser.set_defaults(handler=handler)


def baseline_model_factory_main(
    model_name: str,
    task_type: str = "classification",
    features: list[dict] | None = None,
    target: str = "target",
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """Generate sklearn baseline model code with pipelines."""
    if output_dir is None:
        output_dir = get_output_dir("baseline_model_factory")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)

    if features is None:
        features = [
            {"name": "feature_1", "type": "numeric"},
            {"name": "feature_2", "type": "numeric"},
            {"name": "feature_3", "type": "categorical"},
        ]

    try:
        # Generate training script
        train_code = generate_train_script(model_name, task_type, features, target)
        write_text(content=train_code, filename="train.py", skill_name="baseline_model_factory")

        # Generate config
        config = generate_config(model_name, task_type, features, target)
        write_text(content=config, filename="config.yaml", skill_name="baseline_model_factory")

        # Generate evaluation script
        eval_code = generate_eval_script(model_name, task_type)
        write_text(content=eval_code, filename="evaluate.py", skill_name="baseline_model_factory")

        # Generate README
        readme = generate_readme(model_name, task_type)
        write_text(content=readme, filename="README.md", skill_name="baseline_model_factory")

        return {
            "success": True,
            "output_dir": str(output_dir),
            "files": ["train.py", "config.yaml", "evaluate.py", "README.md"],
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_train_script(
    model_name: str, task_type: str, features: list[dict], target: str
) -> str:
    """Generate training script with sklearn pipelines."""
    numeric_features = [f["name"] for f in features if f.get("type") == "numeric"]
    categorical_features = [f["name"] for f in features if f.get("type") == "categorical"]

    if task_type == "classification":
        models = """\
    "logistic": LogisticRegression(random_state=RANDOM_STATE, max_iter=1000),
    "random_forest": RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE),
    "gradient_boosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
    "dummy": DummyClassifier(strategy="stratified", random_state=RANDOM_STATE),"""
        imports = """\
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report"""
        eval_metrics = """\
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")
    logger.info(f"Accuracy: {accuracy:.4f}")
    logger.info(f"F1 Score: {f1:.4f}")
    logger.info(f"\\nClassification Report:\\n{classification_report(y_test, y_pred)}")
    return {"accuracy": accuracy, "f1_weighted": f1}"""
    else:
        models = """\
    "linear": LinearRegression(),
    "ridge": Ridge(alpha=1.0, random_state=RANDOM_STATE),
    "random_forest": RandomForestRegressor(n_estimators=100, random_state=RANDOM_STATE),
    "dummy": DummyRegressor(strategy="mean"),"""
        imports = """\
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score"""
        eval_metrics = """\
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    logger.info(f"MSE: {mse:.4f}")
    logger.info(f"MAE: {mae:.4f}")
    logger.info(f"R2: {r2:.4f}")
    return {"mse": mse, "mae": mae, "r2": r2}"""

    return dedent(f'''\
        #!/usr/bin/env python3
        """Training script for {model_name} baseline model.
        
        Generated by skillpack baseline-model-factory on {datetime.now().strftime("%Y-%m-%d %H:%M")}
        """

        import argparse
        import logging
        from pathlib import Path

        import joblib
        import pandas as pd
        import yaml
        from sklearn.compose import ColumnTransformer
        from sklearn.impute import SimpleImputer
        from sklearn.model_selection import train_test_split, cross_val_score
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler, OneHotEncoder
        {imports}

        # Configuration
        RANDOM_STATE = 42
        TEST_SIZE = 0.2
        CV_FOLDS = 5

        # Feature definitions
        NUMERIC_FEATURES = {numeric_features}
        CATEGORICAL_FEATURES = {categorical_features}
        TARGET = "{target}"

        # Set up logging
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        logger = logging.getLogger("{model_name}")


        def get_models() -> dict:
            \"\"\"Define baseline models to train.\"\"\"
            return {{
        {models}
            }}


        def create_preprocessor() -> ColumnTransformer:
            \"\"\"Create preprocessing pipeline.\"\"\"
            numeric_transformer = Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ])

            categorical_transformer = Pipeline([
                ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
                ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
            ])

            return ColumnTransformer([
                ("numeric", numeric_transformer, NUMERIC_FEATURES),
                ("categorical", categorical_transformer, CATEGORICAL_FEATURES),
            ])


        def train_and_evaluate(X_train, X_test, y_train, y_test) -> dict:
            \"\"\"Train all baseline models and evaluate.\"\"\"
            results = {{}}
            preprocessor = create_preprocessor()
            
            for name, model in get_models().items():
                logger.info(f"Training {{name}}...")
                
                pipeline = Pipeline([
                    ("preprocessor", preprocessor),
                    ("model", model),
                ])
                
                # Cross-validation
                cv_scores = cross_val_score(pipeline, X_train, y_train, cv=CV_FOLDS)
                logger.info(f"  CV Score: {{cv_scores.mean():.4f}} (+/- {{cv_scores.std():.4f}})")
                
                # Final training
                pipeline.fit(X_train, y_train)
                y_pred = pipeline.predict(X_test)
                
                # Evaluate
                metrics = evaluate(y_test, y_pred, name)
                metrics["cv_mean"] = cv_scores.mean()
                metrics["cv_std"] = cv_scores.std()
                results[name] = {{
                    "pipeline": pipeline,
                    "metrics": metrics,
                }}
            
            return results


        def evaluate(y_test, y_pred, model_name: str) -> dict:
            \"\"\"Evaluate predictions.\"\"\"
            logger.info(f"Results for {{model_name}}:")
        {eval_metrics}


        def main():
            parser = argparse.ArgumentParser(description="Train baseline models")
            parser.add_argument("--data", type=Path, required=True, help="Path to training data CSV")
            parser.add_argument("--output", type=Path, default=Path("./models"), help="Output directory")
            parser.add_argument("--model", default="random_forest", help="Model to save as primary")
            args = parser.parse_args()

            # Load data
            logger.info(f"Loading data from {{args.data}}")
            df = pd.read_csv(args.data)
            
            X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
            y = df[TARGET]
            
            # Split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
            )
            logger.info(f"Train size: {{len(X_train)}}, Test size: {{len(X_test)}}")

            # Train and evaluate
            results = train_and_evaluate(X_train, X_test, y_train, y_test)

            # Save best model
            args.output.mkdir(parents=True, exist_ok=True)
            best_pipeline = results[args.model]["pipeline"]
            model_path = args.output / f"{{args.model}}_model.pkl"
            joblib.dump(best_pipeline, model_path)
            logger.info(f"Saved model to {{model_path}}")

            # Save metrics summary
            metrics_summary = {{name: r["metrics"] for name, r in results.items()}}
            with open(args.output / "metrics.yaml", "w") as f:
                yaml.dump(metrics_summary, f)
            logger.info(f"Saved metrics to {{args.output / 'metrics.yaml'}}")


        if __name__ == "__main__":
            main()
    ''')


def generate_config(
    model_name: str, task_type: str, features: list[dict], target: str
) -> str:
    """Generate configuration YAML."""
    return yaml.dump(
        {
            "model": {
                "name": model_name,
                "task": task_type,
                "version": "1.0.0",
            },
            "features": features,
            "target": target,
            "training": {
                "test_size": 0.2,
                "random_state": 42,
                "cv_folds": 5,
            },
            "models": {
                "classification": ["logistic", "random_forest", "gradient_boosting"],
                "regression": ["linear", "ridge", "random_forest"],
            },
        },
        default_flow_style=False,
    )


def generate_eval_script(model_name: str, task_type: str) -> str:
    """Generate evaluation script."""
    return dedent(f'''\
        #!/usr/bin/env python3
        """Evaluation script for {model_name} model.
        
        Generated by skillpack baseline-model-factory on {datetime.now().strftime("%Y-%m-%d %H:%M")}
        """

        import argparse
        from pathlib import Path

        import joblib
        import pandas as pd
        {"from sklearn.metrics import accuracy_score, classification_report" if task_type == "classification" else "from sklearn.metrics import mean_squared_error, r2_score"}


        def main():
            parser = argparse.ArgumentParser(description="Evaluate model on new data")
            parser.add_argument("--model", type=Path, required=True, help="Path to saved model")
            parser.add_argument("--data", type=Path, required=True, help="Path to evaluation data")
            parser.add_argument("--target", default="target", help="Target column name")
            args = parser.parse_args()

            # Load model
            pipeline = joblib.load(args.model)

            # Load data
            df = pd.read_csv(args.data)
            feature_cols = [c for c in df.columns if c != args.target]
            X = df[feature_cols]
            y = df[args.target]

            # Predict
            y_pred = pipeline.predict(X)

            # Metrics
            {"print(f'Accuracy: {accuracy_score(y, y_pred):.4f}')" if task_type == "classification" else "print(f'MSE: {mean_squared_error(y, y_pred):.4f}')"}
            {"print(classification_report(y, y_pred))" if task_type == "classification" else "print(f'R2: {r2_score(y, y_pred):.4f}')"}


        if __name__ == "__main__":
            main()
    ''')


def generate_readme(model_name: str, task_type: str) -> str:
    """Generate README documentation."""
    return dedent(f'''\
        # {model_name} Baseline Model

        Generated by skillpack baseline-model-factory on {datetime.now().strftime("%Y-%m-%d %H:%M")}

        ## Task Type
        {task_type.title()}

        ## Usage

        ### Training
        ```bash
        python train.py --data data.csv --output ./models --model random_forest
        ```

        ### Evaluation
        ```bash
        python evaluate.py --model models/random_forest_model.pkl --data test.csv
        ```

        ## Files
        - `train.py` - Training script with cross-validation
        - `evaluate.py` - Evaluation script
        - `config.yaml` - Model configuration

        ## Models Trained
        {"- Logistic Regression (baseline)\\n- Random Forest\\n- Gradient Boosting\\n- Dummy Classifier (stratified)" if task_type == "classification" else "- Linear Regression\\n- Ridge Regression\\n- Random Forest\\n- Dummy Regressor (mean)"}

        ## Configuration
        Edit `config.yaml` to customize:
        - Feature definitions
        - Train/test split
        - Cross-validation folds
    ''')
