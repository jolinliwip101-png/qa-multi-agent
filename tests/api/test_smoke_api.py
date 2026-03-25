import pytest
import requests

BASE_URL = "https://automationexercise.com"


class TestSmokeAPI:
    """Minimal API smoke tests for automationexercise.com"""

    def test_get_products_list(self):
        """GET /api/productsList — verify 200 and products in response"""
        resp = requests.get(f"{BASE_URL}/api/productsList", timeout=10)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        data = resp.json()
        assert "products" in data or len(data) > 0, "Response should contain products"

    def test_post_verify_login_invalid_credentials(self):
        """POST /api/verifyLogin with invalid creds — verify failure response"""
        payload = {"email": "invalid@test.com", "password": "wrongpassword"}
        resp = requests.post(f"{BASE_URL}/api/verifyLogin", data=payload, timeout=10)
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("responseCode") == 404, f"Expected responseCode 404 for invalid creds, got: {body}"
        assert "not found" in body.get("message", "").lower(), f"Expected 'not found' in message: {body}"

    def test_get_brands_list(self):
        """GET /api/brandsList — verify 200"""
        resp = requests.get(f"{BASE_URL}/api/brandsList", timeout=10)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
