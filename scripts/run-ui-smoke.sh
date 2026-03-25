#!/bin/bash
# Run Playwright UI smoke tests against automationexercise.com
set -e
cd "$(dirname "$0")/.."
npx playwright test --config=playwright.config.ts
