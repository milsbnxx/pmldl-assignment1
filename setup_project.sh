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
  echo "Python 3.10-3.13 is required. On macOS with Homebrew: brew install python@3.13"
  exit 1
fi

echo "Using $PYTHON_BIN ($($PYTHON_BIN --version))"
rm -rf "$ROOT/.venv"
"$PYTHON_BIN" -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/python" -m pip install --upgrade pip
"$ROOT/.venv/bin/pip" install -r "$ROOT/requirements.txt"

echo "Project environment is ready: $ROOT/.venv"
