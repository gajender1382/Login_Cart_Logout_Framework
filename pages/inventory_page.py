"""Inventory page — product list and cart actions after login."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utilities.testConstants import INVENTORY_PAGE_TITLE


class InventoryPage(BasePage):
    PRODUCTS_TITLE = (By.CLASS_NAME, "title")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")  # small number on cart icon

    def get_products_title(self):
        """Returns page heading — should be 'Products' after login."""
        return self.get_text(self.PRODUCTS_TITLE)

    def is_inventory_page_displayed(self):
        """True when the inventory page heading matches the expected title."""
        return self.get_products_title() == INVENTORY_PAGE_TITLE

    def click_add_to_cart(self, button_id):
        """Click Add to Cart for a product (button id comes from Excel)."""
        self.scroll_and_click((By.ID, button_id))

    def get_cart_badge_count(self):
        """Returns how many items are in the cart (e.g. '1')."""
        return self.wait_visible(self.CART_BADGE).text
