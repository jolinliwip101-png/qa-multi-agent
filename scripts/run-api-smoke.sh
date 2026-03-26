#!/bin/bash
# Run API smoke tests
# Stack: Python + httpx + pytest + Allure
set -e
cd "$(dirname "$0")/.."
VENV="./venv311/bin/python"
[ ! -x "$VENV" ] && VENV="python3"
$VENV -m pytest tests/api/ -m api -v --tb=short "$@"
