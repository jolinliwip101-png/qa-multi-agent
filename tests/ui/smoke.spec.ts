import { test, expect } from '@playwright/test';

test.describe('UI Smoke Tests', () => {
  test('homepage loads and products navigation works', async ({ page }) => {
    // 1. Open the homepage
    await page.goto('/');

    // 2. Verify title contains "Automation Exercise"
    await expect(page).toHaveTitle(/Automation Exercise/);

    // 2b. Dismiss cookie consent if it appears
    const consentBtn = page.locator('.fc-primary-button, #CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll, .cookie-consent button').first();
    if (await consentBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await consentBtn.click();
      await page.waitForTimeout(500);
    }

    // 3. Click "Products"
    await page.getByRole('link', { name: 'Products' }).first().click();

    // 4. Verify URL contains /products
    await expect(page).toHaveURL(/\/products/);

    // 5. Verify the product list section is visible
    await expect(page.locator('.features_items')).toBeVisible();
  });
});
