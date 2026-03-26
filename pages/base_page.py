"""
pages/base_page.py — Base Page Object with shared functionality.
"""
from typing import Optional

from playwright.sync_api import Page, Locator, TimeoutError as PWTimeoutError


class BasePage:
    """Base class for all Page Objects. Provides common navigation and assertion helpers."""

    def __init__(self, page: Page, base_url: str = "https://www.automationexercise.com"):
        self.page = page
        self.base_url = base_url

    # ------------------------------------------------------------------ #
    # Navigation
    # ------------------------------------------------------------------ #
    def open(self, path: str = "/") -> "BasePage":
        """Navigate to a path under the base URL."""
        self.page.goto(f"{self.base_url}{path}")
        return self

    def get_current_url(self) -> str:
        return self.page.url

    def wait_for_url_contains(self, fragment: str, timeout: float = 10_000) -> None:
        self.page.wait_for_url(f"**/{fragment}**", timeout=timeout)

    # ------------------------------------------------------------------ #
    # Visibility helpers
    # ------------------------------------------------------------------ #
    def is_visible(self, selector: str, timeout: float = 5_000) -> bool:
        """Return True if the selector is visible within the timeout."""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except PWTimeoutError:
            return False

    def wait_for_element(
        self, selector: str, timeout: float = 10_000
    ) -> Locator:
        return self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    def dismiss_cookie_consent(self, timeout: float = 5_000) -> None:
        """Dismiss cookie consent / GDPR banner if present."""
        # Wait for the banner to appear before trying to dismiss it
        consent_btn = self.page.locator("button.fc-cta-consent, button.fc-primary-button")
        try:
            consent_btn.first.wait_for(state="visible", timeout=timeout)
            consent_btn.first.click(timeout=timeout)
            # Wait for banner to disappear
            self.page.locator(".fc-consent-root").wait_for(state="hidden", timeout=5_000)
            self.page.wait_for_timeout(300)
        except Exception:
            pass  # No banner present — continue normally

    def click(self, selector: str, timeout: float = 10_000) -> None:
        self.page.click(selector, timeout=timeout)

    def fill(self, selector: str, value: str, timeout: float = 10_000) -> None:
        self.page.fill(selector, value, timeout=timeout)

    def type_text(
        self, selector: str, text: str, delay: int = 100, timeout: float = 10_000
    ) -> None:
        self.page.type_(selector, text, delay=delay, timeout=timeout)

    def get_text(self, selector: str, timeout: float = 10_000) -> str:
        return self.page.wait_for_selector(selector, state="visible", timeout=timeout).inner_text()

    def get_attribute(
        self, selector: str, attr: str, timeout: float = 10_000
    ) -> Optional[str]:
        return self.page.get_attribute(
            self.page.wait_for_selector(selector, state="attached", timeout=timeout),
            attr,
        )

    # ------------------------------------------------------------------ #
    # Scrolling
    # ------------------------------------------------------------------ #
    def scroll_to_element(self, selector: str) -> None:
        self.page.evaluate(f"document.querySelector('{selector}').scrollIntoView()")

    def scroll_by(self, x: int = 0, y: int = 500) -> None:
        self.page.evaluate(f"window.scrollBy({x}, {y})")

    # ------------------------------------------------------------------ #
    # Assertions shortcuts
    # ------------------------------------------------------------------ #
    def assert_url_contains(self, fragment: str) -> "BasePage":
        assert fragment in self.page.url, (
            f"URL '{self.page.url}' does not contain '{fragment}'"
        )
        return self

    def assert_title_contains(self, text: str) -> "BasePage":
        assert text in self.page.title(), (
            f"Page title '{self.page.title()}' does not contain '{text}'"
        )
        return self

    def assert_element_visible(self, selector: str) -> "BasePage":
        assert self.is_visible(selector), f"Element '{selector}' is not visible"
        return self

    def assert_element_not_visible(self, selector: str) -> "BasePage":
        assert not self.is_visible(selector), (
            f"Element '{selector}' should not be visible but it is"
        )
        return self
