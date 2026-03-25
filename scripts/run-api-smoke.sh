#!/bin/bash
# Run API smoke tests against automationexercise.com
set -e
cd "$(dirname "$0")/.."
./venv/bin/python -m pytest tests/api/test_smoke_api.py -v
