"""Full flow helper — login, add to cart, logout in one function."""

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from utilities.browserHelper import reset_to_login_page
from utilities.readExcel import ReadExcel


def run_login_add_to_cart_logout(driver, product_row_index=0):
    """Run the complete flow: Login → Add to cart → Logout.

    Args:
        driver: Selenium WebDriver from conftest fixture
        product_row_index: which product row to use from Excel (0 = first)

    Returns:
        (product dict, cart badge count as string)
    """
    # Step 1 — clear cookies and open a clean login page
    reset_to_login_page(driver)
    LoginPage(driver).login(ReadExcel.get_username(), ReadExcel.get_password())

    # Step 2 — add one product and read the cart badge
    product = ReadExcel.get_product(product_row_index)
    InventoryPage(driver).click_add_to_cart(product["add_to_cart_id"])
    cart_count = InventoryPage(driver).get_cart_badge_count()

    # Step 3 — log out via hamburger menu
    LogoutPage(driver).logout()

    return product, cart_count
