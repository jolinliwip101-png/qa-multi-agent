/**
 * LEGACY / ORPHANED — Do not use.
 *
 * The UI test stack has migrated to Python + pytest-playwright.
 * TypeScript Playwright tests have been archived to tests/ui/_archive/.
 *
 * This file is kept for reference only. The active config is pytest.ini.
 */
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/ui/_archive',
  timeout: 30000,
  use: {
    baseURL: 'https://www.automationexercise.com',
    headless: true,
  },
});
