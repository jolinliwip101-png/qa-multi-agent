"""
pages/__init__.py — Page Object package.
"""
from .home_page import HomePage
from .products_page import ProductsPage
from .login_page import LoginPage
from .cart_page import CartPage
from .base_page import BasePage

__all__ = ["HomePage", "ProductsPage", "LoginPage", "CartPage", "BasePage"]
