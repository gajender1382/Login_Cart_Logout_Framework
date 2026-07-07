"""Pytest fixtures and hooks — shared setup for all tests.

How fixtures connect (pytest runs these automatically):

  browser          ← reads --browser from command line (chrome / firefox)
       ↓
  driver           ← opens browser before test, closes after test
       ↓
  login_in_driver  ← optional: navigates to app and logs in (uses Excel credentials)

Each test picks what it needs in its method signature:
  def test_x(self, driver):           → fresh browser, not logged in
  def test_y(self, login_in_driver):  → browser already on inventory page
"""

import shutil
import tempfile

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.login_page import LoginPage
from utilities.readExcel import ReadExcel
from utilities.readProperties import ReadConfig
from utilities.screenshotHelper import ScreenshotHelper

_SUPPORTED_BROWSERS = {"chrome", "firefox"}


def _create_chrome_driver():
    """Start Chrome with a temp profile to avoid 'Change your password' popup."""
    options = ChromeOptions()
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-notifications")
    options.add_argument(
        "--disable-features=PasswordLeakDetection,PasswordCheck,"
        "PasswordProtectionForSignedInUsers,PasswordManagerOnboarding"
    )
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )
    driver = webdriver.Chrome(options=options)
    driver._chrome_user_data_dir = user_data_dir
    return driver


def _create_firefox_driver():
    """Start Firefox with password-save prompts disabled."""
    options = FirefoxOptions()
    options.set_preference("signon.rememberSignons", False)
    return webdriver.Firefox(options=options)


def pytest_addoption(parser):
    """Add --browser option so run.bat can pass chrome or firefox."""
    parser.addoption("--browser", default="chrome", help="Browser: chrome or firefox")


@pytest.fixture
def browser(request):
    """Read --browser from command line (used by driver fixture)."""
    value = request.config.getoption("--browser").lower()
    if value not in _SUPPORTED_BROWSERS:
        pytest.fail(f"Unsupported browser: '{value}'. Use: chrome, firefox")
    return value


@pytest.fixture()
def driver(browser):
    """Open browser before test, close browser after test.

    yield = code before runs at START of test, code after runs at END (teardown).
    """
    if browser == "firefox":
        driver = _create_firefox_driver()
    else:
        driver = _create_chrome_driver()
    driver.maximize_window()
    driver.implicitly_wait(10)  # Selenium waits up to 10s when finding elements
    yield driver
    driver.quit()  # always close browser, even if test fails
    user_data_dir = getattr(driver, "_chrome_user_data_dir", None)
    if user_data_dir:
        shutil.rmtree(user_data_dir, ignore_errors=True)


@pytest.fixture
def login_in_driver(driver):
    """Open app and log in with default user from Excel before the test."""
    driver.get(ReadConfig.getApplicationURL())
    LoginPage(driver).login(ReadExcel.get_username(), ReadExcel.get_password())
    yield driver


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook — runs after each test phase (setup / call / teardown).

    When the test body fails, grab the WebDriver from fixtures and save a screenshot
    to Screenshots/ so you can see what the page looked like at failure time.
    """
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return  # only screenshot on actual test failure, not setup errors
    for fixture_name in ("login_in_driver", "driver"):
        driver = item.funcargs.get(fixture_name)
        if driver:
            screenshot_name = item.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
            try:
                ScreenshotHelper.save_fail(driver, screenshot_name)
            except Exception:
                pass  # don't hide the original test failure if screenshot fails
            break
