"""Browser helper — reset session to a clean login page."""

from utilities.readProperties import ReadConfig


def reset_to_login_page(driver):
    """Go to login page with no active session.

    Used before each flow so the previous login does not affect the next step.
    We visit the URL twice: first load sets cookies, delete_all_cookies clears them,
    second load gives a fresh unauthenticated session.
    """
    driver.get(ReadConfig.getApplicationURL())
    driver.delete_all_cookies()
    driver.get(ReadConfig.getApplicationURL())
