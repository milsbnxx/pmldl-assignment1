from pathlib import Path

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

PROJECT_DIR = Path(__file__).resolve().parents[3]
PROJECT_PYTHON = PROJECT_DIR / ".venv" / "bin" / "python"

with DAG(
    dag_id="pmldl_mlops_pipeline",
    description="Data engineering -> model engineering -> Docker deployment",
    schedule="*/5 * * * *",
    start_date=pendulum.datetime(2026, 9, 1, tz="UTC"),
    catchup=False,
    max_active_runs=1,
    tags=["pmldl", "mlops", "assignment1"],
) as dag:
    stage_1 = BashOperator(
        task_id="stage_1_data_engineering",
        bash_command=f'"{PROJECT_PYTHON}" "{PROJECT_DIR / "code/datasets/prepare_data.py"}"',
    )

    stage_2 = BashOperator(
        task_id="stage_2_model_engineering",
        bash_command=f'"{PROJECT_PYTHON}" "{PROJECT_DIR / "code/models/train_model.py"}"',
    )

    stage_3 = BashOperator(
        task_id="stage_3_deployment",
        bash_command=(
            "set -e; "
            "command -v docker >/dev/null || { echo 'Docker CLI not found'; exit 1; }; "
            "docker info >/dev/null 2>&1 || { echo 'Docker Desktop is not running'; exit 1; }; "
            f'cd "{PROJECT_DIR}" && docker compose up -d --build'
        ),
    )

    verify = BashOperator(
        task_id="verify_deployment",
        bash_command=f'"{PROJECT_PYTHON}" "{PROJECT_DIR / "scripts/verify_deployment.py"}"',
    )

    stage_1 >> stage_2 >> stage_3 >> verify
