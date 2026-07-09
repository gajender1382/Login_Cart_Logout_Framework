"""Logout test — verify user returns to login page after logout."""

from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from utilities.readProperties import ReadConfig
from utilities.screenshotHelper import ScreenshotHelper


def test_logout(login_in_driver, test_logger):
    """After logout, URL and login form should confirm the user is logged out."""
    test_logger.info("Starting: logout flow")

    LogoutPage(login_in_driver).logout()

    current_url = login_in_driver.current_url.rstrip("/")
    expected_url = ReadConfig.getApplicationURL().rstrip("/")
    assert current_url == expected_url
    assert LoginPage(login_in_driver).is_login_page_displayed()

    path = ScreenshotHelper.save_success(login_in_driver, "test_logout")
    test_logger.info(f"Screenshot: {path}")
    test_logger.info("Ending: logout test")
