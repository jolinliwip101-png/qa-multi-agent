#!/bin/bash
# Run full smoke suite (UI + API)
# Stack: Python + pytest + Playwright + httpx + Allure
set -e
cd "$(dirname "$0")/.."
VENV="./venv311/bin/python"
[ ! -x "$VENV" ] && VENV="python3"
$VENV -m pytest -m smoke -v --tb=short "$@"
