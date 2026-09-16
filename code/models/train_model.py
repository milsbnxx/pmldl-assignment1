from pathlib import Path
import json
from datetime import datetime, timezone

import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]

TRAIN_PATH = (
    ROOT
    / "data"
    / "processed"
    / "train.csv"
)

TEST_PATH = (
    ROOT
    / "data"
    / "processed"
    / "test.csv"
)

MODEL_PATH = (
    ROOT
    / "models"
    / "model.joblib"
)

METRICS_PATH = (
    ROOT
    / "metrics"
    / "metrics.json"
)

TARGET = "target"


def main() -> None:
    train_df = pd.read_csv(
        TRAIN_PATH
    )

    test_df = pd.read_csv(
        TEST_PATH
    )

    if TARGET not in train_df.columns:
        raise ValueError(
            f"Target '{TARGET}' missing from train data."
        )

    if TARGET not in test_df.columns:
        raise ValueError(
            f"Target '{TARGET}' missing from test data."
        )

    # Use ALL available features.
    feature_columns = [
        column
        for column in train_df.columns
        if column != TARGET
    ]

    if len(feature_columns) == 0:
        raise ValueError(
            "No feature columns found."
        )

    missing_in_test = [
        feature
        for feature in feature_columns
        if feature not in test_df.columns
    ]

    if missing_in_test:
        raise ValueError(
            f"Features missing from test data: "
            f"{missing_in_test}"
        )

    X_train = train_df[
        feature_columns
    ]

    y_train = train_df[
        TARGET
    ]

    X_test = test_df[
        feature_columns
    ]

    y_test = test_df[
        TARGET
    ]

    # -----------------------------
    # Feature transformation
    # + model
    # -----------------------------

    pipeline = Pipeline(
        steps=[
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )

    pipeline.fit(
        X_train,
        y_train,
    )

    # -----------------------------
    # Evaluation
    # -----------------------------

    predictions = pipeline.predict(
        X_test
    )

    probabilities = (
        pipeline
        .predict_proba(X_test)[:, 1]
    )

    metrics = {
        "accuracy": float(
            accuracy_score(
                y_test,
                predictions,
            )
        ),
        "precision": float(
            precision_score(
                y_test,
                predictions,
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                y_test,
                predictions,
                zero_division=0,
            )
        ),
        "f1": float(
            f1_score(
                y_test,
                predictions,
                zero_division=0,
            )
        ),
        "roc_auc": float(
            roc_auc_score(
                y_test,
                probabilities,
            )
        ),
        "train_rows": int(
            len(train_df)
        ),
        "test_rows": int(
            len(test_df)
        ),
        "number_of_features": int(
            len(feature_columns)
        ),
        "evaluated_at_utc": (
            datetime
            .now(timezone.utc)
            .isoformat()
        ),
    }

    # -----------------------------
    # Feature metadata for API/app
    # -----------------------------

    feature_defaults = {
        feature: float(
            X_train[feature].median()
        )
        for feature in feature_columns
    }

    feature_min = {
        feature: float(
            X_train[feature].min()
        )
        for feature in feature_columns
    }

    feature_max = {
        feature: float(
            X_train[feature].max()
        )
        for feature in feature_columns
    }

    artifact = {
        "model": pipeline,
        "features": feature_columns,
        "target": TARGET,
        "class_names": {
            0: "malignant",
            1: "benign",
        },
        "feature_defaults": feature_defaults,
        "feature_min": feature_min,
        "feature_max": feature_max,
    }

    # -----------------------------
    # Save model + metrics
    # -----------------------------

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    METRICS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        artifact,
        MODEL_PATH,
    )

    METRICS_PATH.write_text(
        json.dumps(
            metrics,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print("MODEL ENGINEERING COMPLETED")
    print("---------------------------")

    print(
        f"Train rows: {len(train_df)}"
    )

    print(
        f"Test rows: {len(test_df)}"
    )

    print(
        f"Features: {len(feature_columns)}"
    )

    print()

    for metric_name, value in metrics.items():
        if isinstance(value, float):
            print(
                f"{metric_name}: "
                f"{value:.4f}"
            )

    print()
    print(
        f"Saved model: {MODEL_PATH}"
    )

    print(
        f"Saved metrics: {METRICS_PATH}"
    )


if __name__ == "__main__":
    main()