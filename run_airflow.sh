#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV="$ROOT/.airflow-venv"

if [[ ! -x "$VENV/bin/airflow" ]]; then
  echo "Airflow environment is missing. Run ./setup_airflow.sh first."
  exit 1
fi

source "$VENV/bin/activate"
export AIRFLOW_HOME="$ROOT/services/airflow"
export AIRFLOW__CORE__DAGS_FOLDER="$ROOT/services/airflow/dags"
export AIRFLOW__CORE__LOAD_EXAMPLES="False"
export AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION="False"
# Keep Homebrew/Docker Desktop locations visible to Airflow child processes.
export PATH="$VENV/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

echo "Starting Airflow standalone..."
echo "UI: http://localhost:8080"
echo "DAG: pmldl_mlops_pipeline"
echo "The generated admin password will be printed below."
exec airflow standalone
