"""
conftest.py — Shared pytest fixtures for the automationexercise.com test suite.
"""
import os
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_URL = os.getenv("BASE_URL", "https://www.automationexercise.com")
API_BASE_URL = os.getenv("API_BASE_URL", "https://automationexercise.com/api")

# Test credentials — override via environment variables if needed
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "vicky_smoke_test@example.com")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "Test@1234")


# ---------------------------------------------------------------------------
# Browser / Page fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def playwright_instance():
    """Session-scoped Playwright instance (browser binary is launched once)."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance) -> Browser:
    """Launch Chromium (headless by default). Set HEADED=1 to see the browser."""
    headed = os.getenv("HEADED", "0") == "1"
    browser = playwright_instance.chromium.launch(headless=not headed)
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def browser_context(browser: Browser, browser_context_args) -> BrowserContext:
    """Default browser context shared across all UI tests in a session."""
    ctx = browser.new_context(**browser_context_args)
    yield ctx
    ctx.close()


@pytest.fixture
def page(browser_context: BrowserContext) -> Page:
    """Fresh page for each test. Automatically closed after the test."""
    page = browser_context.new_page()
    yield page
    page.close()


# ---------------------------------------------------------------------------
# API client fixture
# ---------------------------------------------------------------------------
@pytest.fixture
def api_client():
    """Returns an httpx client pointed at the API base URL."""
    import httpx

    with httpx.Client(base_url=API_BASE_URL, timeout=15.0) as client:
        yield client


# ---------------------------------------------------------------------------
# Session-scoped state for cross-test data sharing
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def shared_test_data():
    """Dictionary that can hold data shared across tests in the session."""
    return {}


# ---------------------------------------------------------------------------
# Browser context args — run once before each browser context is created
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def browser_context_args():
    """Default arguments passed to every new browser context."""
    return {
        "viewport": {"width": 1280, "height": 720},
        "locale": "en-GB",
        "ignore_https_errors": True,
    }


# ---------------------------------------------------------------------------
# Navigation helper
# ---------------------------------------------------------------------------
@pytest.fixture
def navigate_to(page: Page):
    """Helper to navigate to a path under BASE_URL."""

    def _navigate(path: str):
        page.goto(f"{BASE_URL}{path}")

    return _navigate
