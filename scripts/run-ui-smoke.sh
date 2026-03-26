#!/bin/bash
# Run Python Playwright UI smoke tests
# Stack: Python + pytest-playwright + Allure
set -e
cd "$(dirname "$0")/.."
VENV="./venv311/bin/python"
[ ! -x "$VENV" ] && VENV="python3"
$VENV -m pytest tests/ui/ -m ui -v --tb=short "$@"
