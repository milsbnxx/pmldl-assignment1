# Assignment requirement mapping

| Assignment requirement | Implementation |
|---|---|
| Raw data input | `data/raw/breast_cancer.csv` |
| Load and clean data | `code/datasets/prepare_data.py` |
| Missing-value handling | Median imputation in Stage 1 |
| Outlier removal | IQR-based removal in Stage 1 |
| Train/test split | Stratified 80/20 split |
| Feature engineering | Standardization with `StandardScaler` |
| Train a model | Logistic Regression |
| Evaluate/log metrics | `metrics/metrics.json` |
| Save trained model | `models/model.joblib` |
| Model API | FastAPI on port 8000 |
| Web app | Streamlit on port 8501 |
| Separate Docker containers | `docker-compose.yml` has `api` and `app` services |
| Full automated pipeline | Airflow DAG |
| Every 5 minutes | DAG schedule `*/5 * * * *` |
