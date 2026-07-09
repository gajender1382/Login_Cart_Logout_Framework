"""Add to cart tests — verify cart badge updates for products from Excel."""

import pytest

from pages.inventory_page import InventoryPage
from utilities.readExcel import ReadExcel
from utilities.screenshotHelper import ScreenshotHelper
from utilities.testConstants import INITIAL_CART_COUNT


def _product_indices():
    """Build parametrize ids from Excel product rows."""
    return list(range(ReadExcel.get_product_count()))


@pytest.mark.parametrize("product_row_index", _product_indices())
def test_add_product_to_cart(login_in_driver, product_row_index, test_logger):
    """Each product from Excel should show cart badge '1' after adding."""
    product = ReadExcel.get_product(product_row_index)
    test_logger.info(f"Starting: add to cart for {product['name']}")

    inventory = InventoryPage(login_in_driver)
    inventory.click_add_to_cart(product["add_to_cart_id"])
    cart_count = inventory.get_cart_badge_count()

    assert cart_count == INITIAL_CART_COUNT
    safe_name = product["add_to_cart_id"].replace("-", "_")
    path = ScreenshotHelper.save_success(login_in_driver, f"test_add_to_cart_{safe_name}")
    test_logger.info(f"Screenshot: {path}")
    test_logger.info("Ending: add to cart test")
