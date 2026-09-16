import os
from pathlib import Path

import joblib
import pandas as pd

from fastapi import (
    FastAPI,
    HTTPException,
)

from pydantic import BaseModel


MODEL_PATH = Path(
    os.getenv(
        "MODEL_PATH",
        "/app/models/model.joblib",
    )
)


if not MODEL_PATH.exists():
    raise RuntimeError(
        f"Model file not found: "
        f"{MODEL_PATH}"
    )


artifact = joblib.load(
    MODEL_PATH
)

model = artifact[
    "model"
]

features = artifact[
    "features"
]

class_names = artifact[
    "class_names"
]

feature_defaults = artifact.get(
    "feature_defaults",
    {},
)

feature_min = artifact.get(
    "feature_min",
    {},
)

feature_max = artifact.get(
    "feature_max",
    {},
)


app = FastAPI(
    title="PMLDL Breast Cancer Prediction API",
    version="2.0.0",
)


class PredictionRequest(BaseModel):
    features: dict[str, float]


@app.get("/")
def root() -> dict:
    return {
        "message": (
            "Breast Cancer Prediction API"
        )
    }


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "model_loaded": True,
        "number_of_features": len(
            features
        ),
    }


@app.get("/metadata")
def metadata() -> dict:
    return {
        "features": features,
        "feature_defaults": (
            feature_defaults
        ),
        "feature_min": (
            feature_min
        ),
        "feature_max": (
            feature_max
        ),
        "class_names": (
            class_names
        ),
    }


@app.get("/features")
def feature_info() -> dict:
    return {
        "features": features,
    }


@app.post("/predict")
def predict(
    payload: PredictionRequest,
) -> dict:

    received_features = (
        payload.features
    )

    missing_features = [
        feature
        for feature in features
        if feature
        not in received_features
    ]

    extra_features = [
        feature
        for feature
        in received_features
        if feature
        not in features
    ]

    if missing_features:
        raise HTTPException(
            status_code=422,
            detail={
                "message": (
                    "Missing required features"
                ),
                "missing_features": (
                    missing_features
                ),
            },
        )

    if extra_features:
        raise HTTPException(
            status_code=422,
            detail={
                "message": (
                    "Unknown features received"
                ),
                "extra_features": (
                    extra_features
                ),
            },
        )

    ordered_values = {
        feature: float(
            received_features[
                feature
            ]
        )
        for feature in features
    }

    row = pd.DataFrame(
        [
            ordered_values
        ],
        columns=features,
    )

    prediction = int(
        model.predict(
            row
        )[0]
    )

    probabilities = (
        model.predict_proba(
            row
        )[0]
    )

    classifier_classes = (
        model
        .named_steps[
            "classifier"
        ]
        .classes_
    )

    probability_by_class = {
        int(class_id): float(
            probability
        )
        for class_id, probability
        in zip(
            classifier_classes,
            probabilities,
        )
    }

    return {
        "prediction": prediction,
        "class_name": class_names[
            prediction
        ],
        "probability_malignant": (
            probability_by_class
            .get(
                0,
                0.0,
            )
        ),
        "probability_benign": (
            probability_by_class
            .get(
                1,
                0.0,
            )
        ),
    }