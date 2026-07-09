"""Login tests — verify successful login reaches the inventory page."""

from pages.inventory_page import InventoryPage
from utilities.screenshotHelper import ScreenshotHelper
from utilities.testConstants import INVENTORY_PAGE_TITLE


def test_inventory_after_login(login_in_driver, test_logger):
    """After login, the inventory page title should be 'Products'."""
    test_logger.info("Starting: login and verify inventory page")

    inventory = InventoryPage(login_in_driver)
    assert inventory.is_inventory_page_displayed()
    assert inventory.get_products_title() == INVENTORY_PAGE_TITLE

    path = ScreenshotHelper.save_success(login_in_driver, "test_login_inventory")
    test_logger.info(f"Screenshot: {path}")
    test_logger.info("Ending: login test")
