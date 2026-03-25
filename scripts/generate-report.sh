#!/bin/bash
# Generate test report from pytest or Playwright results
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p reports

# Copy existing results if available
if [ -f test-results/.last-run.json ]; then
  cp test-results/.last-run.json reports/report.json
  echo "Report: reports/report.json (from test-results)"
  exit 0
fi

# Run pytest with HTML report fallback
PYTEST="python3"
[ -x ./venv/bin/python ] && PYTEST="./venv/bin/python"

if $PYTEST -m pytest --co -q >/dev/null 2>&1; then
  $PYTEST -m pytest --html=reports/pytest-report.html --self-contained-html 2>/dev/null || \
    $PYTEST -m pytest -v --tb=short 2>&1 | tee reports/pytest-output.txt
  echo "Report: reports/pytest-report.html"
else
  echo "No tests found — skipping report generation"
fi
