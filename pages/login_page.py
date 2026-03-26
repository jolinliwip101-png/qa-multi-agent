"""
pages/login_page.py — Page Object for the Login / Signup page (/login).
"""
import allure
from playwright.sync_api import Page

from locators.registry import (
    LOGIN_EMAIL_INPUT,
    LOGIN_PASSWORD_INPUT,
    LOGIN_SUBMIT_BTN,
    LOGIN_FORM,
    LOGIN_PAGE_HEADING,
    SIGNUP_NAME_INPUT,
    SIGNUP_EMAIL_INPUT,
    SIGNUP_SUBMIT_BTN,
    SIGNUP_PAGE_HEADING,
    NAV_HOME_LINK,
)
from .base_page import BasePage


class LoginPage(BasePage):
    """Interactions on the Login / Signup page (/login)."""

    URL = "/login"

    def __init__(self, page: Page):
        super().__init__(page, base_url="https://www.automationexercise.com")
        self.page = page

    @allure.step("Open Login page")
    def open(self) -> "LoginPage":
        super().open(self.URL)
        self.page.wait_for_load_state("domcontentloaded")
        self.dismiss_cookie_consent()
        return self

    @allure.step("Verify Login page loaded")
    def verify_page_loaded(self) -> "LoginPage":
        self.assert_element_visible(LOGIN_FORM)
        return self
        return self

    @allure.step("Login with email: {email}")
    def login(self, email: str, password: str) -> "LoginPage":
        """Fill and submit the login form."""
        self.fill(LOGIN_EMAIL_INPUT, email)
        self.fill(LOGIN_PASSWORD_INPUT, password)
        self.click(LOGIN_SUBMIT_BTN)
        self.page.wait_for_load_state("networkidle", timeout=15_000)
        return self

    @allure.step("Verify user is logged in (check nav logout link)")
    def verify_logged_in(self) -> "LoginPage":
        """After login, the nav should show 'Logout' instead of 'Signup / Login'."""
        from locators.registry import NAV_LOGOUT_LINK

        self.assert_element_visible(NAV_LOGOUT_LINK)
        return self

    @allure.step("Verify login error is shown")
    def verify_login_error(self) -> "LoginPage":
        """Check that an error message appears for invalid credentials."""
        error_locator = ".login-form .alert-danger, .alert-danger"
        assert self.is_visible(error_locator), (
            "Expected login error alert to be visible for invalid credentials"
        )
        return self

    @allure.step("Fill signup form (name: {name}, email: {email})")
    def fill_signup_form(self, name: str, email: str) -> "LoginPage":
        """Pre-fill the signup new-user form (without submitting)."""
        self.fill(SIGNUP_NAME_INPUT, name)
        self.fill(SIGNUP_EMAIL_INPUT, email)
        return self

    @allure.step("Go back to home")
    def go_to_home(self):
        from .home_page import HomePage

        self.click(NAV_HOME_LINK)
        return HomePage(self.page)
