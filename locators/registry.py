"""
locators/registry.py — Centralised CSS / XPath selectors for automationexercise.com.

All page objects import from here so selectors are defined in one place.
Naming convention: PAGE_ELEMENT (all caps with underscores).
"""
from playwright.sync_api import Page, Locator


# ===========================================================================
# HOME PAGE
# ===========================================================================
HOME_LOGO = "img[src='/static/images/home/logo.png']"
HOME_SLIDER_IMAGES = "#slider .item"
HOME_FEATURE_ITEMS = ".single-products"
HOME_CATEGORY_SECTION = ".category-products"
HOME_SUBSCRIPTION_EMAIL_INPUT = "#susbscribe_email"
HOME_SUBSCRIPTION_BUTTON = "button#subscribe"
HOME_FOOTER_TEXT = "footer.footer"


# ===========================================================================
# PRODUCTS PAGE
# ===========================================================================
PRODUCTS_PAGE_HEADING = "h2.title.text-center"
PRODUCTS_SEARCH_INPUT = "input#search_product"
PRODUCTS_SEARCH_SUBMIT_BTN = "button#submit_search"
PRODUCT_SEARCH_FORM = "form#search_product_form"
PRODUCT_CARDS = ".single-products"
PRODUCT_NAMES = ".productinfo p"
PRODUCT_ADD_TO_CART_BTN = ".add-to-cart"
PRODUCT_OVERLAY_ADD_TO_CART_BTN = ".overlay-content .add-to-cart"


# ===========================================================================
# PRODUCT DETAIL PAGE
# ===========================================================================
PRODUCT_DETAIL_NAME = ".product-information h2"
PRODUCT_DETAIL_PRICE = ".product-information span span"
PRODUCT_DETAIL_ADD_TO_CART = "button.cart"
PRODUCT_DETAIL_QUANTITY_INPUT = "#quantity"


# ===========================================================================
# CART PAGE
# ===========================================================================
CART_PAGE_HEADING = "#cart_items"
CART_ITEMS = "tbody tr"
CART_EMPTY_MESSAGE = "p.text-center"
CART_PRODUCT_LINK = "a[href^='/product_details']"
CART_DELETE_BTN = ".cart_delete a[data-product-id]"
CART_CONTINUE_SHOPPING_BTN = ".btn-success"


# ===========================================================================
# LOGIN / SIGNUP PAGE
# ===========================================================================
LOGIN_EMAIL_INPUT = "input[data-qa='login-email']"
LOGIN_PASSWORD_INPUT = "input[data-qa='login-password']"
LOGIN_SUBMIT_BTN = "button[data-qa='login-button']"
LOGIN_FORM = ".login-form"
SIGNUP_NAME_INPUT = "input[data-qa='signup-name']"
SIGNUP_EMAIL_INPUT = "input[data-qa='signup-email']"
SIGNUP_SUBMIT_BTN = "button[data-qa='signup-button']"
LOGIN_PAGE_HEADING = ".login-form h2"
SIGNUP_PAGE_HEADING = ".signup-form h2"
LOGGED_IN_USER_MENU = "a[i-class='fa fa-user']"


# ===========================================================================
# NAVIGATION BAR
# ===========================================================================
NAV_HOME_LINK = "a[href='/']"
NAV_PRODUCTS_LINK = "a[href='/products']"
NAV_CART_LINK = "a[href='/view_cart']"
NAV_LOGIN_LINK = "a[href='/login']"
NAV_LOGOUT_LINK = "a[href='/logout']"
NAV_LOGGED_IN_USER = ".navbar-nav li a[i-class='fa fa-user']"


# ===========================================================================
# FOOTER / SUBSCRIPTION
# ===========================================================================
FOOTER_SUBSCRIBE_EMAIL = "#susbscribe_email"
FOOTER_SUBSCRIBE_BTN = "button#subscribe"
FOOTER_SUBSCRIBE_SUCCESS = ".footer-top .alert-success"


# ===========================================================================
# CHECKOUT PAGE
# ===========================================================================
CHECKOUT_HEADING = ".checkout-page h2"
CHECKOUT_ADDRESS_BOX = ".checkout-step .address"
CHECKOUT_CONTINUE_BTN = ".btn-default.checkout"


# ===========================================================================
# BRANDS PAGE
# ===========================================================================
BRAND_LINKS = ".brands-name a"
BRAND_PRODUCT_ITEMS = ".product-image-wrapper"


# ===========================================================================
# SEARCH RESULTS
# ===========================================================================
SEARCH_RESULTS_HEADING = "h2.title"
SEARCH_PRODUCT_CARDS = ".single-products"
SEARCH_NO_RESULT = ".product-information p"
