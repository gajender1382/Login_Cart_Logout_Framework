"""Logout test — verify user returns to login page after logout.

Flow:
  1. conftest logs in first (login_in_driver)
  2. Open hamburger menu → click Logout
  3. Assert browser is back on the login URL from config.ini
"""

from pages.logout_page import LogoutPage
from utilities.customLogger import LogGeneration
from utilities.readProperties import ReadConfig
from utilities.screenshotHelper import ScreenshotHelper


class Test_Logout:
    logger = LogGeneration.log_generation()
    TEST_FILE = "test_logout"

    def test_logout(self, login_in_driver):
        self.logger.info("Starting: logout flow")

        # LogoutPage opens sidebar menu and clicks the logout link
        LogoutPage(login_in_driver).logout()

        # After logout, URL should match the app home / login page
        current_url = login_in_driver.current_url.rstrip("/")
        expected_url = ReadConfig.getApplicationURL().rstrip("/")
        assert current_url == expected_url

        path = ScreenshotHelper.save_success(login_in_driver, f"{self.TEST_FILE}_logout")
        self.logger.info(f"Screenshot: {path}")
        self.logger.info("Ending: logout test")
