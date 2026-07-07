"""Negative login tests — invalid credentials and locked-out user."""

import pytest

from pages.login_page import LoginPage
from utilities.readExcel import ReadExcel
from utilities.readProperties import ReadConfig
from utilities.testConstants import LOGIN_ERROR_LOCKED_OUT, LOGIN_ERROR_WRONG_CREDENTIALS


@pytest.fixture
def login_page(driver):
    """Open the app login page before each negative login test."""
    driver.get(ReadConfig.getApplicationURL())
    return LoginPage(driver)


def test_wrong_password_shows_error(login_page, test_logger):
    """Wrong password should show an error and stay on the login page."""
    user = ReadExcel.get_user("standard_user")
    test_logger.info("Starting: wrong password login test")

    login_page.login(user["username"], "wrong_password")
    error_text = login_page.get_error_message()

    assert LOGIN_ERROR_WRONG_CREDENTIALS in error_text
    assert login_page.is_login_page_displayed()
    test_logger.info("Ending: wrong password login test")


def test_locked_out_user_shows_error(login_page, test_logger):
    """Locked-out user should see an error and cannot reach inventory."""
    user = ReadExcel.get_user("locked_out_user")
    test_logger.info("Starting: locked out user login test")

    login_page.login(user["username"], user["password"])
    error_text = login_page.get_error_message()

    assert LOGIN_ERROR_LOCKED_OUT in error_text
    assert login_page.is_login_page_displayed()
    test_logger.info("Ending: locked out user login test")
