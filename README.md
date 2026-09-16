# PMLDL Assignment 1 — Automated MLOps Pipeline

This repository implements the three required assignment stages:

1. **Data Engineering** — load raw data, handle missing values, remove outliers, split into train/test, save processed files.
2. **Model Engineering** — standardize selected features, train a logistic-regression classifier, evaluate it, save metrics and the trained model.
3. **Deployment** — run a FastAPI model API and a Streamlit web application in **separate Docker containers**.

Apache Airflow orchestrates the complete pipeline every 5 minutes.

## Dataset

The project uses the **Breast Cancer Wisconsin Diagnostic dataset distributed with scikit-learn**. A CSV copy is committed at `data/raw/breast_cancer.csv`, so Stage 1 always starts from a raw file artifact.

This dataset is not one of the two datasets prohibited by the assignment.

## Repository structure

```text
.
├── code
│   ├── datasets/prepare_data.py
│   ├── models/train_model.py
│   └── deployment
│       ├── api
│       │   ├── Dockerfile
│       │   ├── main.py
│       │   └── requirements.txt
│       └── app
│           ├── Dockerfile
│           ├── app.py
│           └── requirements.txt
├── data
│   ├── raw/breast_cancer.csv
│   └── processed/
├── models/model.joblib
├── metrics/metrics.json
├── scripts/verify_deployment.py
├── services/airflow/dags/mlops_pipeline.py
├── docker-compose.yml
├── setup_project.sh
├── setup_airflow.sh
├── run_pipeline.sh
└── run_airflow.sh
```

## Prerequisites

- macOS/Linux
- Python **3.10–3.13** (Python 3.13 is recommended)
- Docker Desktop

On macOS:

```bash
brew install python@3.13
```

## 1. Set up the ML project

```bash
./setup_project.sh
```

This creates `.venv` using a supported Python version and installs the ML dependencies.

## 2. Start Docker Desktop

Open Docker Desktop and wait until the Docker engine is running. Check:

```bash
docker info
```

## 3. Test the complete pipeline without Airflow

```bash
./run_pipeline.sh
```

The script runs data processing, model training/evaluation, Docker deployment, and health checks.

Open:

- FastAPI docs: http://localhost:8000/docs
- Streamlit app: http://localhost:8501

Check containers:

```bash
docker compose ps
```

Both `pmldl_assignment_api` and `pmldl_assignment_app` should be running.

Stop deployment:

```bash
docker compose down
```

## 4. Install Airflow

```bash
./setup_airflow.sh
```

Airflow is installed in a **separate** `.airflow-venv` so it does not conflict with the ML project environment.

## 5. Run Airflow

Keep Docker Desktop running, then:

```bash
./run_airflow.sh
```

Open:

- Airflow UI: http://localhost:8080
- DAG: `pmldl_mlops_pipeline`

Airflow standalone prints the generated admin password in the terminal.

The DAG is scheduled every five minutes and contains:

```text
stage_1_data_engineering
        ↓
stage_2_model_engineering
        ↓
stage_3_deployment
        ↓
verify_deployment
```

The Docker build uses normal Docker layer caching. The first build can take a few minutes because dependencies are downloaded; later builds should be much faster unless requirements change.

## Outputs

Stage 1 creates:

- `data/processed/train.csv`
- `data/processed/test.csv`
- `data/processed/data_report.json`

Stage 2 creates:

- `models/model.joblib`
- `metrics/metrics.json`

Stage 3 creates two running services:

- API container on port `8000`
- Streamlit container on port `8501`

## Useful troubleshooting

### `docker compose ps` shows only the app

Inspect all containers and API logs:

```bash
docker compose ps -a
docker compose logs api --tail=100
```

### Docker is installed but Airflow deployment fails

Verify Docker Desktop is running:

```bash
docker info
```

### Airflow does not support Python 3.14

Use Python 3.13:

```bash
brew install python@3.13
PYTHON_BIN=python3.13 ./setup_airflow.sh
```

## Submission

Submit the link to the **public GitHub repository**. During the TA demonstration, show:

1. the Airflow DAG and successful task run;
2. processed train/test artifacts;
3. saved metrics and model;
4. two running Docker containers;
5. FastAPI `/docs`;
6. a prediction made from the Streamlit application.
