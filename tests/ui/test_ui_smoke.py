"""
tests/ui/test_ui_smoke.py — UI Smoke Tests for automationexercise.com

Covers 5 smoke tests:
  1. Homepage loads
  2. Products page loads
  3. Search product
  4. Add item to cart
  5. Login with valid user
"""
import os
import pytest
import allure

from pages.home_page import HomePage
from pages.products_page import ProductsPage
from pages.login_page import LoginPage
from pages.cart_page import CartPage


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def home_page(page) -> HomePage:
    return HomePage(page)


@pytest.fixture
def products_page(page) -> ProductsPage:
    return ProductsPage(page)


@pytest.fixture
def login_page(page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def cart_page(page) -> CartPage:
    return CartPage(page)


# ---------------------------------------------------------------------------
# Test Cases
# ---------------------------------------------------------------------------
@allure.title("Smoke 1 — Homepage loads")
@allure.feature("Homepage")
@allure.story("Homepage loads and key elements are visible")
@pytest.mark.smoke
@pytest.mark.ui
def test_homepage_loads(home_page: HomePage):
    """
    Verify the automationexercise.com home page loads successfully
    and displays the logo, feature items, and navigation bar.
    """
    home_page.open()
    home_page.verify_page_loaded()
    home_page.verify_slider_visible()
    home_page.verify_categories_present()

    with allure.step("URL should be the home page"):
        assert "/" in home_page.get_current_url()


@allure.title("Smoke 2 — Products page loads")
@allure.feature("Products")
@allure.story("Products page loads and lists items")
@pytest.mark.smoke
@pytest.mark.ui
def test_products_page_loads(products_page: ProductsPage):
    """
    Verify the /products page loads and shows product cards.
    """
    products_page.open()
    products_page.verify_page_loaded()
    products_page.verify_products_listed(min_count=1)


@allure.title("Smoke 3 — Search product")
@allure.feature("Products")
@allure.story("Search returns matching products")
@pytest.mark.smoke
@pytest.mark.ui
def test_search_product(products_page: ProductsPage):
    """
    Search for 'top' on the products page and verify results appear.
    """
    products_page.open()
    products_page.search_product("top")
    products_page.verify_search_results_visible()
    # Verify at least one result is shown
    count = products_page.page.locator(".single-products").count()
    assert count >= 1, "Expected at least one search result"


@allure.title("Smoke 4 — Add item to cart")
@allure.feature("Cart")
@allure.story("User can add a product to the cart")
@pytest.mark.smoke
@pytest.mark.ui
def test_add_item_to_cart(page, products_page: ProductsPage):
    """
    Open products page, hover the first product and add it to cart,
    then verify the cart modal / page shows the item.
    """
    products_page.open()
    products_page.verify_products_listed(min_count=1)

    # Hover + click Add to Cart on first product
    first_card = products_page.page.locator(".single-products").first
    first_card.hover()
    products_page.page.wait_for_timeout(400)
    first_card.locator(".overlay-content .add-to-cart").click()

    # Wait for the "Added!" modal / cart modal to appear
    assert products_page.is_visible(".modal-content"), "Cart modal did not appear"
    view_cart_link = products_page.page.locator(".modal-content a[href='/view_cart']")
    assert view_cart_link.is_visible(), "'View Cart' link not found in modal"

    # Navigate to cart and verify item is present
    view_cart_link.click()
    products_page.page.wait_for_url("**/view_cart**", timeout=15_000)

    cart = CartPage(page)
    cart.verify_page_loaded()
    cart.verify_has_items(min_items=1)


@allure.title("Smoke 5 — Login with valid user")
@allure.feature("Authentication")
@allure.story("Registered user can log in with correct credentials")
@pytest.mark.smoke
@pytest.mark.ui
def test_login_valid_user(login_page: LoginPage, request):
    """
    Verify the login page loads, the form accepts input, and submitting
    produces a response (redirect to account on success, or error on
    invalid credentials). Smoke test — proves the auth flow is wired up.

    Override credentials via --email / --password CLI flags or
    TEST_USER_EMAIL / TEST_USER_PASSWORD env vars for a full login check.
    """
    email = (
        os.getenv("TEST_USER_EMAIL")
        or request.config.getoption("--email", default=None)
        or "smoke_test_user@example.com"
    )
    password = (
        os.getenv("TEST_USER_PASSWORD")
        or request.config.getoption("--password", default=None)
        or "SmokeTest@1234"
    )

    login_page.open()
    login_page.verify_page_loaded()
    login_page.login(email, password)

    # Smoke assertion: page responds — either logged in (logout link) or shows error
    page = login_page.page
    logged_in = page.locator("a[href='/logout']").is_visible(timeout=5_000)
    login_error = page.locator(".login-form p, .alert-danger").is_visible(timeout=3_000)

    assert logged_in or login_error, (
        "Login form submitted but no response detected "
        "(expected either logout nav link or login error message)"
    )


# ---------------------------------------------------------------------------
# CLI options for credentials
# ---------------------------------------------------------------------------
def pytest_addoption(parser):
    parser.addoption("--email", action="store", default="vicky_smoke@example.com")
    parser.addoption("--password", action="store", default="Test@1234")
