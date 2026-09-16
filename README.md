# PMLDL Assignment 1 — MLOps Pipeline

This project implements a simple end-to-end MLOps pipeline for a binary classification problem.

The model is trained on the Breast Cancer Wisconsin dataset from scikit-learn. The goal of the model is to predict whether a tumor is benign or malignant based on numerical features.

The project includes data processing, model training and evaluation, deployment with FastAPI and Streamlit, Docker containers, and pipeline automation with Apache Airflow.

## Project structure

```text
.
├── code
│   ├── datasets
│   │   └── prepare_data.py
│   ├── models
│   │   └── train_model.py
│   └── deployment
│       ├── api
│       │   ├── main.py
│       │   └── Dockerfile
│       └── app
│           ├── app.py
│           └── Dockerfile
├── data
│   ├── raw
│   │   └── breast_cancer.csv
│   └── processed
│       ├── train.csv
│       ├── test.csv
│       └── data_report.json
├── models
│   └── model.joblib
├── metrics
│   └── metrics.json
├── services
│   └── airflow
│       └── dags
│           └── mlops_pipeline.py
├── docker-compose.yml
├── requirements.txt
├── requirements-airflow.txt
├── setup_project.sh
├── setup_airflow.sh
├── run_pipeline.sh
├── run_airflow.sh
└── README.md
```

## Dataset

The project uses the Breast Cancer Wisconsin dataset available in `scikit-learn`.

The original dataset contains 569 rows and 30 numerical features.

During the data engineering stage:

- the data is loaded from `data/raw/breast_cancer.csv`;
- missing values are handled;
- extreme outliers are removed using the IQR method;
- the data is split into training and testing sets.

After preprocessing, the current split contains approximately:

- 410 training rows;
- 103 testing rows.

## Model

The model is a Logistic Regression classifier.

Before training, all numerical features are standardized using `StandardScaler`.

The scaler and the classifier are stored together in a scikit-learn Pipeline, which is then saved to:

```text
models/model.joblib
```

The following metrics are calculated on the test set:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

The latest metrics are stored in:

```text
metrics/metrics.json
```

The model currently achieves around 0.99 accuracy and a recall close to 1.0.

## Deployment

The model is exposed through a FastAPI service.

The web interface is implemented with Streamlit.

They run in separate Docker containers and communicate with each other through Docker Compose.

After starting the project:

FastAPI documentation is available at:

```text
http://localhost:8000/docs
```

Streamlit application is available at:

```text
http://localhost:8501
```

The Streamlit app allows the user to enter feature values and receive a prediction from the model API.

## Running the project

Make sure Python and Docker Desktop are installed.

First, create the project environment:

```bash
./setup_project.sh
```

Then start the complete pipeline:

```bash
./run_pipeline.sh
```

This script:

1. processes the dataset;
2. trains and evaluates the model;
3. saves the trained model and metrics;
4. builds the Docker images;
5. starts the API and Streamlit containers;
6. checks that the services are available.

You can check the running containers with:

```bash
docker compose ps
```

To stop them:

```bash
docker compose down
```

## Airflow

Apache Airflow is used to automate the pipeline.

Airflow has a DAG called:

```text
pmldl_mlops_pipeline
```

The DAG contains the following tasks:

```text
stage_1_data_engineering
        ↓
stage_2_model_engineering
        ↓
stage_3_deployment
        ↓
verify_deployment
```

The pipeline is scheduled to run every 5 minutes.

To install Airflow:

```bash
./setup_airflow.sh
```

To start it:

```bash
./run_airflow.sh
```

The Airflow interface is available at:

```text
http://localhost:8080
```

The generated admin password is printed in the terminal when Airflow starts.

## Technologies

The main tools used in this project are:

- Python
- pandas
- scikit-learn
- FastAPI
- Streamlit
- Docker
- Docker Compose
- Apache Airflow


