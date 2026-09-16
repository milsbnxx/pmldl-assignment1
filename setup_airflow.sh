#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"

choose_python() {
  for candidate in python3.13 python3.12 python3.11 python3.10; do
    if command -v "$candidate" >/dev/null 2>&1; then
      echo "$candidate"
      return 0
    fi
  done
  return 1
}

PYTHON_BIN="${PYTHON_BIN:-$(choose_python || true)}"
if [[ -z "$PYTHON_BIN" ]]; then
  echo "Airflow 3.1.8 needs Python 3.10-3.13. On macOS: brew install python@3.13"
  exit 1
fi

PYVER="$($PYTHON_BIN -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
case "$PYVER" in
  3.10|3.11|3.12|3.13) ;;
  *) echo "Unsupported Python for Airflow: $PYVER"; exit 1 ;;
esac

VENV="$ROOT/.airflow-venv"
rm -rf "$VENV"
"$PYTHON_BIN" -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-3.1.8/constraints-${PYVER}.txt"
"$VENV/bin/pip" install -r "$ROOT/requirements-airflow.txt" --constraint "$CONSTRAINT_URL"

echo "Airflow environment is ready: $VENV"
echo "Run ./run_airflow.sh"
