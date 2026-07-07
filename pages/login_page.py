"""Login page — username, password, and Login button."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    # Locators: (how to find, value) — keep all selectors in one place
    USERNAME = (By.NAME, "user-name")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.NAME, "login-button")

    def login(self, username, password):
        """Clear fields, type credentials, and click Login."""
        username_field = self.wait_visible(self.USERNAME)
        username_field.clear()
        username_field.send_keys(username)

        password_field = self.wait_visible(self.PASSWORD)
        password_field.clear()
        password_field.send_keys(password)

        self.click(self.LOGIN_BUTTON)
