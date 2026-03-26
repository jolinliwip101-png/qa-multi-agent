"""
pages/home_page.py — Page Object for the automationexercise.com home page.
"""
import allure
from playwright.sync_api import Page

from locators.registry import (
    HOME_LOGO,
    HOME_FEATURE_ITEMS,
    HOME_SUBSCRIPTION_EMAIL_INPUT,
    HOME_SUBSCRIPTION_BUTTON,
    HOME_FOOTER_TEXT,
    NAV_PRODUCTS_LINK,
    NAV_LOGIN_LINK,
    NAV_CART_LINK,
)
from .base_page import BasePage


class HomePage(BasePage):
    """Interactions available on the home / landing page."""

    URL = "/"

    def __init__(self, page: Page):
        super().__init__(page, base_url="https://www.automationexercise.com")
        self.page = page

    # ------------------------------------------------------------------ #
    # Navigation
    # ------------------------------------------------------------------ #
    @allure.step("Open home page")
    def open(self) -> "HomePage":
        super().open(self.URL)
        self.page.wait_for_load_state("domcontentloaded")
        self.dismiss_cookie_consent()
        return self

    # ------------------------------------------------------------------ #
    # Page content assertions
    # ------------------------------------------------------------------ #
    @allure.step("Verify home page has loaded")
    def verify_page_loaded(self) -> "HomePage":
        """Assert that key home page elements are present."""
        self.assert_element_visible(HOME_LOGO)
        self.assert_element_visible(HOME_FEATURE_ITEMS)
        return self

    @allure.step("Verify slider images are visible")
    def verify_slider_visible(self) -> "HomePage":
        """Confirm the hero slider section is visible."""
        assert self.is_visible("#slider"), "Hero slider section not found"
        return self

    @allure.step("Verify category sections are present")
    def verify_categories_present(self) -> "HomePage":
        """Confirm category navigation section is rendered."""
        assert self.is_visible(".left-sidebar"), "Category sidebar not found"
        return self

    # ------------------------------------------------------------------ #
    # Navigation actions
    # ------------------------------------------------------------------ #
    @allure.step("Navigate to Products page")
    def go_to_products(self):
        from .products_page import ProductsPage

        self.click(NAV_PRODUCTS_LINK)
        self.wait_for_url_contains("products")
        return ProductsPage(self.page)

    @allure.step("Navigate to Login/Signup page")
    def go_to_login(self):
        from .login_page import LoginPage

        self.click(NAV_LOGIN_LINK)
        self.wait_for_url_contains("login")
        return LoginPage(self.page)

    @allure.step("Navigate to Cart page")
    def go_to_cart(self):
        from .cart_page import CartPage

        self.click(NAV_CART_LINK)
        self.wait_for_url_contains("view_cart")
        return CartPage(self.page)

    # ------------------------------------------------------------------ #
    # Subscription
    # ------------------------------------------------------------------ #
    @allure.step("Subscribe to newsletter with email: {email}")
    def subscribe_newsletter(self, email: str) -> "HomePage":
        self.scroll_to_element(HOME_SUBSCRIPTION_EMAIL_INPUT)
        self.fill(HOME_SUBSCRIPTION_EMAIL_INPUT, email)
        self.click(HOME_SUBSCRIPTION_BUTTON)
        return self

    @allure.step("Verify newsletter subscription success message")
    def verify_subscription_success(self) -> "HomePage":
        assert self.is_visible(".alert-success"), (
            "Newsletter subscription success message not visible"
        )
        return self
