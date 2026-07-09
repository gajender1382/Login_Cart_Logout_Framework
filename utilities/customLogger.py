"""Write test logs to console and Logs/Automation_Logs.log."""

import logging
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOG_FORMAT = "%(asctime)s : %(levelname)s : %(message)s"
_DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"


def _configure_console_encoding():
    """Avoid UnicodeEncodeError on Windows/Jenkins console (cp1252)."""
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError, ValueError):
        pass


class LogGeneration:
    @staticmethod
    def log_generation():
        """Return the shared logger used by all tests."""
        logger = logging.getLogger("AutomationLogger")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            _configure_console_encoding()
            os.makedirs(os.path.join(_PROJECT_ROOT, "Logs"), exist_ok=True)

            file_handler = logging.FileHandler(
                os.path.join(_PROJECT_ROOT, "Logs", "Automation_Logs.log"),
                encoding="utf-8",
            )
            file_handler.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))
            logger.addHandler(file_handler)

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))
            logger.addHandler(console_handler)

        return logger
