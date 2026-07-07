"""Inventory page — product list shown after successful login."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class InventoryPage(BasePage):
    PRODUCTS_TITLE = (By.CLASS_NAME, "title")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")  # small number on cart icon

    def get_products_title(self):
        """Returns page heading — should be 'Products' after login."""
        return self.get_text(self.PRODUCTS_TITLE)

    def get_cart_badge_count(self):
        """Returns how many items are in the cart (e.g. '1')."""
        return self.wait_visible(self.CART_BADGE).text
