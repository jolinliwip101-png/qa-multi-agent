"""
pages/cart_page.py — Page Object for the Cart page (/view_cart).
"""
import allure
from playwright.sync_api import Page

from locators.registry import (
    CART_PAGE_HEADING,
    CART_ITEMS,
    CART_EMPTY_MESSAGE,
    CART_PRODUCT_LINK,
    CART_DELETE_BTN,
    CART_CONTINUE_SHOPPING_BTN,
)
from .base_page import BasePage


class CartPage(BasePage):
    """Interactions on the Shopping Cart page (/view_cart)."""

    URL = "/view_cart"

    def __init__(self, page: Page):
        super().__init__(page, base_url="https://www.automationexercise.com")
        self.page = page

    @allure.step("Open Cart page")
    def open(self) -> "CartPage":
        super().open(self.URL)
        return self

    @allure.step("Verify Cart page loaded")
    def verify_page_loaded(self) -> "CartPage":
        self.assert_element_visible(CART_PAGE_HEADING)
        return self

    @allure.step("Verify cart has items")
    def verify_has_items(self, min_items: int = 1) -> "CartPage":
        count = self.page.locator(CART_ITEMS).count()
        assert count >= min_items, f"Expected ≥{min_items} cart items, found {count}"
        return self

    @allure.step("Verify cart is empty")
    def verify_empty(self) -> "CartPage":
        self.assert_element_visible(CART_EMPTY_MESSAGE)
        return self

    @allure.step("Get number of items in cart")
    def get_item_count(self) -> int:
        return self.page.locator(CART_ITEMS).count()

    @allure.step("Remove first item from cart")
    def remove_first_item(self) -> "CartPage":
        self.click(CART_DELETE_BTN)
        self.page.wait_for_load_state("networkidle", timeout=10_000)
        return self

    @allure.step("Click Continue Shopping")
    def continue_shopping(self) -> "CartPage":
        self.click(CART_CONTINUE_SHOPPING_BTN)
        return self
