from pathlib import Path

from ..config import Config
from ..constants import Spreadsheets


def get_data_path(config: Config) -> Path:
    return Path(config.data_dir)


def get_excel_path(config: Config) -> Path:
    return get_data_path(config) / "Excel"


def get_json_path(config: Config) -> Path:
    return get_data_path(config) / "json"


def get_paths_weeks(config: Config) -> Path:
    return get_excel_path(config) / "weeks"


def get_paths_excel(config: Config) -> Spreadsheets:
    excel = get_excel_path(config)
    return {
        "DataStore": excel / "DataStore.xlsx",
        "Result": excel / "Result.xlsx",
        "Registration": excel / "Registration.xlsx",
        "List": excel / "List.xlsx",
        "Attendance": excel / "Attendance.xlsx",
        "Assessment": excel / "Assessment.xlsx",
        "Group": excel / "Group.xlsx",
        "Project": excel / "Project.xlsx",
    }
