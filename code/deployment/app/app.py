import os

import requests
import streamlit as st


API_URL = os.getenv(
    "API_URL",
    "http://api:8000",
)


st.set_page_config(
    page_title=(
        "Breast Cancer Predictor"
    ),
    page_icon="ML",
    layout="wide",
)


st.title(
    "Breast Cancer Prediction"
)

st.write(
    "This application sends tumor "
    "measurements to the FastAPI "
    "model service and displays "
    "the model prediction."
)

st.caption(
    "This project is created for "
    "the PMLDL MLOps assignment "
    "and is not a medical "
    "diagnostic system."
)


# ---------------------------------
# Load feature information from API
# ---------------------------------

try:
    metadata_response = requests.get(
        f"{API_URL}/metadata",
        timeout=10,
    )

    metadata_response.raise_for_status()

    metadata = (
        metadata_response.json()
    )

except requests.RequestException as exc:
    st.error(
        "Could not connect to "
        "the model API."
    )

    st.code(
        str(exc)
    )

    st.stop()


features = metadata[
    "features"
]

defaults = metadata.get(
    "feature_defaults",
    {},
)


# ---------------------------------
# Group features
# ---------------------------------

mean_features = [
    feature
    for feature in features
    if feature.startswith(
        "mean "
    )
]

worst_features = [
    feature
    for feature in features
    if feature.startswith(
        "worst "
    )
]

error_features = [
    feature
    for feature in features
    if feature
    not in mean_features
    and feature
    not in worst_features
]


st.write(
    f"Model uses "
    f"**{len(features)} features**."
)


# ---------------------------------
# Input form
# ---------------------------------

values = {}


with st.form(
    "prediction_form"
):

    with st.expander(
        "Mean features",
        expanded=True,
    ):

        columns = st.columns(2)

        for index, feature in enumerate(
            mean_features
        ):

            default_value = float(
                defaults.get(
                    feature,
                    0.0,
                )
            )

            with columns[
                index % 2
            ]:

                values[
                    feature
                ] = st.number_input(
                    feature.title(),
                    value=default_value,
                    format="%.6f",
                    key=f"input_{feature}",
                )

    with st.expander(
        "Error features",
        expanded=False,
    ):

        columns = st.columns(2)

        for index, feature in enumerate(
            error_features
        ):

            default_value = float(
                defaults.get(
                    feature,
                    0.0,
                )
            )

            with columns[
                index % 2
            ]:

                values[
                    feature
                ] = st.number_input(
                    feature.title(),
                    value=default_value,
                    format="%.6f",
                    key=f"input_{feature}",
                )

    with st.expander(
        "Worst features",
        expanded=False,
    ):

        columns = st.columns(2)

        for index, feature in enumerate(
            worst_features
        ):

            default_value = float(
                defaults.get(
                    feature,
                    0.0,
                )
            )

            with columns[
                index % 2
            ]:

                values[
                    feature
                ] = st.number_input(
                    feature.title(),
                    value=default_value,
                    format="%.6f",
                    key=f"input_{feature}",
                )

    submitted = (
        st.form_submit_button(
            "Predict",
            use_container_width=True,
        )
    )


# ---------------------------------
# Prediction
# ---------------------------------

if submitted:

    payload = {
        "features": values
    }

    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=payload,
            timeout=15,
        )

        response.raise_for_status()

        result = response.json()

        prediction = result[
            "class_name"
        ]

        benign_probability = result[
            "probability_benign"
        ]

        malignant_probability = result[
            "probability_malignant"
        ]

        st.success(
            f"Prediction: "
            f"{prediction.upper()}"
        )

        col1, col2 = st.columns(
            2
        )

        with col1:
            st.metric(
                "Benign probability",
                (
                    f"{benign_probability:.2%}"
                ),
            )

        with col2:
            st.metric(
                "Malignant probability",
                (
                    f"{malignant_probability:.2%}"
                ),
            )

    except requests.RequestException as exc:

        st.error(
            "Prediction request failed."
        )

        st.code(
            str(exc)
        )