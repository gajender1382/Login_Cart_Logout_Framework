"""Login test — verify user reaches inventory page after login.

Flow:
  1. conftest opens browser and logs in (login_in_driver fixture)
  2. This test checks the inventory page title is 'Products'
  3. Screenshot saved on success
"""

from pages.inventory_page import InventoryPage
from utilities.customLogger import LogGeneration
from utilities.screenshotHelper import ScreenshotHelper


class Test_Login:
    logger = LogGeneration.log_generation()
    TEST_FILE = "test_login"

    def test_inventory_after_login(self, login_in_driver):
        # login_in_driver = browser already on inventory page (login done in conftest)
        self.logger.info("Starting: login and verify inventory page")

        # Page Object: InventoryPage wraps Selenium calls for the product list page
        title = InventoryPage(login_in_driver).get_products_title()
        assert title == "Products"  # proves login succeeded

        path = ScreenshotHelper.save_success(login_in_driver, f"{self.TEST_FILE}_inventory")
        self.logger.info(f"Screenshot: {path}")
        self.logger.info("Ending: login test")
