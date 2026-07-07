"""Save screenshots on test pass or fail."""

import os
from datetime import datetime

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ScreenshotHelper:
    SCREENSHOT_DIR = os.path.join(_PROJECT_ROOT, "Screenshots")

    @classmethod
    def _save(cls, driver, name, status):
        os.makedirs(cls.SCREENSHOT_DIR, exist_ok=True)
        safe_name = name.replace("/", "_").replace("\\", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(cls.SCREENSHOT_DIR, f"{safe_name}_{status}_{timestamp}.png")
        driver.save_screenshot(file_path)
        return file_path

    @classmethod
    def save_success(cls, driver, name):
        """Call after a test step passes."""
        return cls._save(driver, name, "success")

    @classmethod
    def save_fail(cls, driver, name):
        """Called automatically by conftest when a test fails."""
        return cls._save(driver, name, "fail")
