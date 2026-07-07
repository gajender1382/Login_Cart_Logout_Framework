"""Base page — shared Selenium helpers used by every page class."""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Wait up to 10 seconds for an element before failing
TIMEOUT = 10


class BasePage:
    """All page classes inherit from this — avoids repeating wait/click code.

    Page Object Model: each web page gets its own class with locators + actions.
    Tests never call Selenium directly — they call page methods instead.
    """

    def __init__(self, driver):
        self.driver = driver  # WebDriver passed in from conftest fixture

    def wait_visible(self, locator):
        """Wait until element is visible on screen, then return it."""
        return WebDriverWait(self.driver, TIMEOUT).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator):
        """Wait until element can be clicked, then return it."""
        return WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator):
        """Wait for clickable element, then click it."""
        self.wait_clickable(locator).click()

    def js_click(self, locator):
        """Click via JavaScript — used when normal click is blocked (e.g. logout link)."""
        self.driver.execute_script("arguments[0].click();", self.wait_visible(locator))

    def get_text(self, locator):
        """Wait for element and return its text."""
        return self.wait_visible(locator).text

    def scroll_and_click(self, locator):
        """Scroll element into view, then click — useful for buttons below the fold."""
        element = self.wait_visible(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()
