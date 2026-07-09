"""Login page — username, password, and Login button."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    # Locators: (how to find, value) — keep all selectors in one place
    USERNAME = (By.NAME, "user-name")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.NAME, "login-button")
    ERROR_BANNER = (By.CSS_SELECTOR, "[data-test='error']")

    def login(self, username, password):
        """Clear fields, type credentials, and click Login."""
        username_field = self.wait_visible(self.USERNAME)
        username_field.clear()
        username_field.send_keys(username)

        password_field = self.wait_visible(self.PASSWORD)
        password_field.clear()
        password_field.send_keys(password)

        self.click(self.LOGIN_BUTTON)

    def is_login_page_displayed(self):
        """True when the login form is visible (used after logout)."""
        return self.wait_visible(self.USERNAME).is_displayed()

    def get_error_message(self):
        """Return login error banner text when credentials are invalid."""
        return self.wait_visible(self.ERROR_BANNER).text
