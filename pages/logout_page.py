"""Logout — open hamburger menu and click Logout."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LogoutPage(BasePage):
    HAMBURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def logout(self):
        """Open sidebar menu and click Logout."""
        self.click(self.HAMBURGER_MENU)
        self.wait_visible(self.LOGOUT_LINK)  # wait for menu to slide open
        self.js_click(self.LOGOUT_LINK)      # JS click avoids sidebar overlay issues
