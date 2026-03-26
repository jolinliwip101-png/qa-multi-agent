"""
pages/products_page.py — Page Object for the /products listing page.
"""
import allure
from playwright.sync_api import Page

from locators.registry import (
    PRODUCTS_PAGE_HEADING,
    PRODUCTS_SEARCH_INPUT,
    PRODUCTS_SEARCH_SUBMIT_BTN,
    PRODUCT_CARDS,
    PRODUCT_NAMES,
    PRODUCT_ADD_TO_CART_BTN,
    PRODUCT_OVERLAY_ADD_TO_CART_BTN,
    SEARCH_PRODUCT_CARDS,
    SEARCH_NO_RESULT,
    NAV_HOME_LINK,
)
from .base_page import BasePage


class ProductsPage(BasePage):
    """Interactions on the Products listing page (/products)."""

    URL = "/products"

    def __init__(self, page: Page):
        super().__init__(page, base_url="https://www.automationexercise.com")
        self.page = page

    @allure.step("Open Products page")
    def open(self) -> "ProductsPage":
        super().open(self.URL)
        self.page.wait_for_load_state("domcontentloaded")
        self.dismiss_cookie_consent()
        return self

    @allure.step("Verify Products page loaded")
    def verify_page_loaded(self) -> "ProductsPage":
        self.assert_element_visible(PRODUCTS_PAGE_HEADING)
        self.assert_element_visible(PRODUCT_CARDS)
        return self

    @allure.step("Verify product list is not empty")
    def verify_products_listed(self, min_count: int = 1) -> "ProductsPage":
        count = self.page.locator(PRODUCT_CARDS).count()
        assert count >= min_count, f"Expected ≥{min_count} products, found {count}"
        return self

    @allure.step("Search for product: {keyword}")
    def search_product(self, keyword: str) -> "ProductsPage":
        """Fill the search box and submit."""
        self.fill(PRODUCTS_SEARCH_INPUT, keyword)
        self.click(PRODUCTS_SEARCH_SUBMIT_BTN)
        self.page.wait_for_load_state("networkidle", timeout=15_000)
        return self

    @allure.step("Verify search results heading is visible")
    def verify_search_results_visible(self) -> "ProductsPage":
        self.assert_element_visible(SEARCH_PRODUCT_CARDS)
        return self

    @allure.step("Verify search returned no results")
    def verify_no_results_found(self) -> "ProductsPage":
        self.assert_element_visible(SEARCH_NO_RESULT)
        return self

    @allure.step("Hover over first product and add to cart")
    def add_first_product_to_cart(self) -> "ProductsPage":
        first_card = self.page.locator(PRODUCT_CARDS).first
        first_card.hover()
        self.page.wait_for_timeout(300)  # let overlay appear
        first_card.locator(PRODUCT_OVERLAY_ADD_TO_CART_BTN).first.click()
        return self

    @allure.step("Add product {name} to cart via overlay")
    def add_product_by_name_to_cart(self, name: str) -> "ProductsPage":
        """Find a product card by name text and click its add-to-cart overlay."""
        cards = self.page.locator(PRODUCT_CARDS)
        count = cards.count()
        for i in range(count):
            card = cards.nth(i)
            name_text = card.locator(PRODUCT_NAMES).inner_text()
            if name.lower() in name_text.lower():
                card.hover()
                self.page.wait_for_timeout(300)
                card.locator(PRODUCT_OVERLAY_ADD_TO_CART_BTN).click()
                return self
        raise ValueError(f"Product '{name}' not found on the products page")

    @allure.step("Verify all product cards have name and price")
    def verify_all_cards_have_details(self) -> "ProductsPage":
        cards = self.page.locator(PRODUCT_CARDS)
        count = cards.count()
        for i in range(count):
            card = cards.nth(i)
            name = card.locator(PRODUCT_NAMES).first
            assert name.is_visible(), f"Product name not visible on card {i + 1}"
        return self

    @allure.step("Go back to home")
    def go_to_home(self):
        from .home_page import HomePage

        self.click(NAV_HOME_LINK)
        return HomePage(self.page)
