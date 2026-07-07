"""Add to cart — click the Add to Cart button on a product."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AddToCartPage(BasePage):
    # Default product: Sauce Labs Backpack
    ADD_TO_CART = (By.ID, "add-to-cart-sauce-labs-backpack")

    def click_add_to_cart(self, button_id=None):
        """Click Add to Cart.

        button_id comes from Excel (Products sheet, column 'Add To Cart ID').
        If not passed, uses the default backpack button.
        """
        locator = (By.ID, button_id) if button_id else self.ADD_TO_CART
        self.scroll_and_click(locator)
