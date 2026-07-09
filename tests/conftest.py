"""Pytest fixtures and hooks — shared setup for all tests.

How fixtures connect (pytest runs these automatically):

  browser          ← chrome / firefox (from --browser, or both for cross-browser runs)
       ↓
  driver           ← opens browser before test, closes after test
       ↓
  login_in_driver  ← optional: navigates to app and logs in (uses Excel credentials)

Parallel execution (pytest-xdist):
  pytest -n auto tests/ --browser chrome  → parallel on Chrome only
  pytest -n auto tests/ --browser both    → parallel on Chrome and Firefox together
"""

import os
import shutil
import tempfile
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.login_page import LoginPage
from utilities.customLogger import LogGeneration
from utilities.readExcel import ReadExcel
from utilities.readProperties import ReadConfig
from utilities.screenshotHelper import ScreenshotHelper

_SUPPORTED_BROWSERS = {"chrome", "firefox"}
_logger = LogGeneration.log_generation()


def _browsers_for_option(browser_option):
    """Map --browser flag to a list of browser names for this run."""
    browser_option = browser_option.lower()
    if browser_option == "both":
        return ["chrome", "firefox"]
    if browser_option in _SUPPORTED_BROWSERS:
        return [browser_option]
    raise pytest.UsageError(
        f"Unsupported --browser value: '{browser_option}'. Use: chrome, firefox, both"
    )


def pytest_addoption(parser):
    """Add --browser option for Chrome, Firefox, or both."""
    parser.addoption(
        "--browser",
        default="chrome",
        help="Browser: chrome, firefox, or both (runs each test on both browsers)",
    )


def pytest_configure(config):
    """Use a unique HTML report name for parallel runs to avoid overwrites."""
    if hasattr(config, "workerinput"):
        return
    numprocesses = getattr(config.option, "numprocesses", None)
    if not numprocesses:
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join("Reports", f"report_parallel_{timestamp}.html")
    config.option.htmlpath = report_path
    os.makedirs("Reports", exist_ok=True)


def pytest_generate_tests(metafunc):
    """Duplicate tests per browser when a test uses a driver-based fixture."""
    driver_fixtures = {"driver", "login_in_driver", "login_page"}
    if not driver_fixtures & set(metafunc.fixturenames):
        return
    browsers = _browsers_for_option(metafunc.config.getoption("--browser"))
    metafunc.parametrize("browser", browsers, indirect=True)


@pytest.fixture
def test_logger():
    """Shared logger for all tests."""
    return _logger


@pytest.fixture
def browser(request):
    """Browser name for this test instance (chrome or firefox)."""
    return request.param


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


@pytest.fixture()
def driver(browser):
    """Open browser before test, close browser after test.

    Uses explicit waits in BasePage only — no implicit wait (avoids slow/flaky tests).
    """
    if browser == "firefox":
        driver = _create_firefox_driver()
    else:
        driver = _create_chrome_driver()
    driver.maximize_window()
    yield driver
    driver.quit()
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
    """Save a screenshot when a test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    for fixture_name in ("login_in_driver", "driver"):
        driver = item.funcargs.get(fixture_name)
        if driver:
            screenshot_name = item.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
            try:
                path = ScreenshotHelper.save_fail(driver, screenshot_name)
                _logger.error(f"Failure screenshot saved: {path}")
            except Exception as exc:
                _logger.error(f"Could not save failure screenshot: {exc}")
            break
