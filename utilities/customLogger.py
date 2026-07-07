"""Write test logs to Logs/Automation_Logs.log."""

import logging
import os

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class LogGeneration:
    @staticmethod
    def log_generation():
        """Return the shared logger used by all test classes."""
        logger = logging.getLogger("AutomationLogger")
        if not logger.handlers:
            logs_dir = os.path.join(_PROJECT_ROOT, "Logs")
            os.makedirs(logs_dir, exist_ok=True)
            handler = logging.FileHandler(os.path.join(logs_dir, "Automation_Logs.log"))
            handler.setFormatter(logging.Formatter(
                fmt="%(asctime)s : %(levelname)s : %(message)s",
                datefmt="%m/%d/%Y %I:%M:%S %p",
            ))
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
