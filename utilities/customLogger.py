"""Write test logs to console and Logs/Automation_Logs.log."""

import logging
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOG_FORMAT = "%(asctime)s : %(levelname)s : %(message)s"
_DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"


class LogGeneration:
    @staticmethod
    def log_generation():
        """Return the shared logger used by all tests."""
        logger = logging.getLogger("AutomationLogger")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            os.makedirs(os.path.join(_PROJECT_ROOT, "Logs"), exist_ok=True)

            file_handler = logging.FileHandler(
                os.path.join(_PROJECT_ROOT, "Logs", "Automation_Logs.log")
            )
            file_handler.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))
            logger.addHandler(file_handler)

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))
            logger.addHandler(console_handler)

        return logger
