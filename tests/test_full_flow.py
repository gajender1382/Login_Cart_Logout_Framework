"""Full flow test — login, add to cart, and logout in one browser session.

Flow:
  1. Uses plain driver (not login_in_driver) — flowHelper does login itself
  2. run_login_add_to_cart_logout() runs all three steps in order
  3. Assert cart count and that we end up back on the login page
"""

from utilities.customLogger import LogGeneration
from utilities.flowHelper import run_login_add_to_cart_logout
from utilities.readProperties import ReadConfig
from utilities.screenshotHelper import ScreenshotHelper


class Test_FullFlow:
    logger = LogGeneration.log_generation()
    TEST_FILE = "test_full_flow"

    def test_login_add_to_cart_logout(self, driver):
        # driver = fresh browser; flowHelper resets session and logs in from scratch
        self.logger.info("Starting: full flow login → add to cart → logout")

        # Returns product details and cart badge text after the full journey
        product, cart_count = run_login_add_to_cart_logout(driver, product_row_index=0)

        assert cart_count == "1"
        current_url = driver.current_url.rstrip("/")
        expected_url = ReadConfig.getApplicationURL().rstrip("/")
        assert current_url == expected_url, "User should be back on login page after logout"

        path = ScreenshotHelper.save_success(driver, f"{self.TEST_FILE}_complete")
        self.logger.info(f"Added {product['name']}, cart count={cart_count}")
        self.logger.info(f"Screenshot: {path}")
        self.logger.info("Ending: full flow test")
