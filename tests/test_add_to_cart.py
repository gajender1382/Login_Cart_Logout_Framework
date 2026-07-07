"""Add to cart test — verify cart badge shows 1 after adding a product.

Flow:
  1. conftest logs in first (login_in_driver)
  2. Read which product to add from Excel (Data/test_data.xlsx)
  3. Click Add to Cart and check the cart badge number
"""

from pages.add_to_cart import AddToCartPage
from pages.inventory_page import InventoryPage
from utilities.customLogger import LogGeneration
from utilities.readExcel import ReadExcel
from utilities.screenshotHelper import ScreenshotHelper


class Test_AddToCart:
    logger = LogGeneration.log_generation()
    TEST_FILE = "test_add_to_cart"

    def test_add_backpack(self, login_in_driver):
        # Row 0 = first product in Excel Products sheet (Sauce Labs Backpack)
        product = ReadExcel.get_product(0)
        self.logger.info(f"Starting: add to cart for {product['name']}")

        # add_to_cart_id is the HTML button id, e.g. add-to-cart-sauce-labs-backpack
        AddToCartPage(login_in_driver).click_add_to_cart(product["add_to_cart_id"])
        cart_count = InventoryPage(login_in_driver).get_cart_badge_count()

        assert cart_count == "1"  # badge on cart icon should show 1 item
        path = ScreenshotHelper.save_success(login_in_driver, f"{self.TEST_FILE}_backpack")
        self.logger.info(f"Screenshot: {path}")
        self.logger.info("Ending: add to cart test")
