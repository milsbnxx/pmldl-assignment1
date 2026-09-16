#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$ROOT/.venv/bin/python"

if [[ ! -x "$PYTHON" ]]; then
  echo "Missing project virtual environment: $ROOT/.venv"
  echo "Run ./setup_project.sh first."
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker CLI is not available. Install/start Docker Desktop first."
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker Desktop is installed but the Docker engine is not running. Start Docker Desktop first."
  exit 1
fi

"$PYTHON" "$ROOT/code/datasets/prepare_data.py"
"$PYTHON" "$ROOT/code/models/train_model.py"
cd "$ROOT"
docker compose up -d --build
"$PYTHON" "$ROOT/scripts/verify_deployment.py"

echo "Pipeline completed successfully."
echo "FastAPI docs: http://localhost:8000/docs"
echo "Streamlit app: http://localhost:8501"
