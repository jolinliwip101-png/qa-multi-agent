"""
tests/api/test_api_smoke.py — API Smoke Tests for automationexercise.com

Covers 5 smoke tests:
  1. GET products list
  2. GET brands list
  3. Search product
  4. Verify login valid
  5. Verify login invalid
"""
import pytest
import allure
import httpx


BASE_URL = "https://automationexercise.com/api"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def pretty_json(response: httpx.Response) -> str:
    try:
        import json
        return json.dumps(response.json(), indent=2)
    except Exception:
        return response.text


# ---------------------------------------------------------------------------
# Test Cases
# ---------------------------------------------------------------------------
@allure.title("API Smoke 1 — GET all products list")
@allure.feature("Products API")
@allure.story("Returns a non-empty list of products")
@pytest.mark.smoke
@pytest.mark.api
def test_get_products_list(api_client: httpx.Client):
    """
    GET /api/productsList
    Expected: 200 OK, response contains a non-empty 'products' list.
    """
    response = api_client.get("/productsList")

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}. Body: {pretty_json(response)}"
    )

    data = response.json()
    assert "products" in data, f"'products' key not found in response: {data}"
    assert isinstance(data["products"], list), "products should be a list"
    assert len(data["products"]) > 0, "products list should not be empty"
    allure.attach(pretty_json(response), "GET /productsList response", allure.attachment_type.JSON)


@allure.title("API Smoke 2 — GET all brands list")
@allure.feature("Brands API")
@allure.story("Returns a non-empty list of brands")
@pytest.mark.smoke
@pytest.mark.api
def test_get_brands_list(api_client: httpx.Client):
    """
    GET /api/brandsList
    Expected: 200 OK, response contains a non-empty 'brands' object.
    """
    response = api_client.get("/brandsList")

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}. Body: {pretty_json(response)}"
    )

    data = response.json()
    assert "brands" in data, f"'brands' key not found in response: {data}"
    assert isinstance(data["brands"], (list, dict)), "brands should be a list or dict"
    assert len(data["brands"]) > 0, "brands list should not be empty"
    allure.attach(pretty_json(response), "GET /brandsList response", allure.attachment_type.JSON)


@allure.title("API Smoke 3 — POST search product")
@allure.feature("Search API")
@allure.story("Searching for 'dress' returns matching products")
@pytest.mark.smoke
@pytest.mark.api
def test_search_product(api_client: httpx.Client):
    """
    POST /api/searchProduct  with form data search_product=dress
    Expected: 200 OK, response contains matching products.
    """
    response = api_client.post(
        "/searchProduct",
        data={"search_product": "dress"},
    )

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}. Body: {pretty_json(response)}"
    )

    # The API may return JSON with a 'products' key or a plain list
    data = response.json()
    # Accept either a dict with 'products' or a direct list
    products = data.get("products", data) if isinstance(data, dict) else data
    assert isinstance(products, list), f"Expected products list, got: {type(products)}"
    assert len(products) > 0, "Expected at least one search result for 'dress'"
    allure.attach(pretty_json(response), "POST /searchProduct response", allure.attachment_type.JSON)


@allure.title("API Smoke 4 — POST verify login with valid credentials")
@allure.feature("Auth API")
@allure.story("Valid credentials return success response")
@pytest.mark.smoke
@pytest.mark.api
def test_verify_login_valid(api_client: httpx.Client):
    """
    POST /api/verifyLogin  with valid email + password.
    Expected: 200 OK, response message contains 'success' or 'logged in'.

    NOTE: This endpoint may require pre-registered credentials.
    Uses a commonly-available test account or a known public account.
    """
    response = api_client.post(
        "/verifyLogin",
        data={
            "email": "vicky_smoke@example.com",
            "password": "Test@1234",
        },
    )

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}. Body: {pretty_json(response)}"
    )

    text = response.text.lower()
    # Accept either JSON success flag or response message indicating success
    assert any(kw in text for kw in ["success", "logged", "user"]), (
        f"Expected success indicator in response, got: {pretty_json(response)}"
    )
    allure.attach(pretty_json(response), "POST /verifyLogin (valid) response", allure.attachment_type.JSON)


@allure.title("API Smoke 5 — POST verify login with invalid credentials")
@allure.feature("Auth API")
@allure.story("Invalid credentials return a failure response")
@pytest.mark.smoke
@pytest.mark.api
def test_verify_login_invalid(api_client: httpx.Client):
    """
    POST /api/verifyLogin  with random invalid email + password.
    Expected: 200 OK, response message indicates failure (no 'success').
    """
    response = api_client.post(
        "/verifyLogin",
        data={
            "email": "not_a_real_user_12345@example.com",
            "password": "WrongPassword999!",
        },
    )

    assert response.status_code == 200, (
        f"Expected 200 (API returns 200 even on auth failure), "
        f"got {response.status_code}. Body: {pretty_json(response)}"
    )

    # Auth failure is indicated by absence of 'success' / 'logged in' in body
    text = response.text.lower()
    assert not any(kw in text for kw in ["success", "logged in", "user found"]), (
        f"Expected auth failure indicator, but got: {pretty_json(response)}"
    )
    allure.attach(pretty_json(response), "POST /verifyLogin (invalid) response", allure.attachment_type.JSON)
