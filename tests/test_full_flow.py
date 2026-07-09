"""Full flow test — login, add to cart, and logout in one browser session."""

from pages.login_page import LoginPage
from utilities.flowHelper import run_login_add_to_cart_logout
from utilities.readProperties import ReadConfig
from utilities.screenshotHelper import ScreenshotHelper
from utilities.testConstants import INITIAL_CART_COUNT


def test_login_add_to_cart_logout(driver, test_logger):
    """End-to-end flow should add a product and return to the login page."""
    test_logger.info("Starting: full flow login → add to cart → logout")

    product, cart_count = run_login_add_to_cart_logout(driver, product_row_index=0)

    assert cart_count == INITIAL_CART_COUNT
    current_url = driver.current_url.rstrip("/")
    expected_url = ReadConfig.getApplicationURL().rstrip("/")
    assert current_url == expected_url
    assert LoginPage(driver).is_login_page_displayed()

    path = ScreenshotHelper.save_success(driver, "test_full_flow_complete")
    test_logger.info(f"Added {product['name']}, cart count={cart_count}")
    test_logger.info(f"Screenshot: {path}")
    test_logger.info("Ending: full flow test")
