"""Read settings from Configurations/config.ini."""

import configparser
import os

# Load config.ini once when this file is imported
config = configparser.RawConfigParser()
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config.read(os.path.join(_project_root, "Configurations", "config.ini"))


class ReadConfig:
    """Reads url, excel path, and default username from config.ini."""

    @staticmethod
    def getApplicationURL():
        return config.get("common info", "url")

    @staticmethod
    def getExcelPath():
        return config.get("common info", "excel_path")

    @staticmethod
    def getDefaultUsername():
        return config.get("common info", "default_username")
