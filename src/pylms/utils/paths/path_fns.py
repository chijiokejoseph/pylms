from pathlib import Path

from pylms.constants import Json, Spreadsheets


def get_data_path() -> Path:
    from pylms.config import read_config

    return Path(read_config().data_dir) / "data"


def get_excel_path() -> Path:
    return get_data_path() / "Excel"


def get_json_path() -> Path:
    return get_data_path() / "Json"


def get_cache_path() -> Path:
    return get_data_path() / ".cache"


def get_paths_weeks() -> Path:
    return get_excel_path() / "weeks"


def get_paths_excel() -> Spreadsheets:
    excel = get_excel_path()
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


def get_paths_json() -> Json:
    json_path = get_json_path()
    return {
        "Classes": json_path / "classes",
        "Records": json_path / "records",
        "Update": json_path / "update",
        "CDS": json_path / "CDS",
        "UpdateForm": json_path / "update",
        "UpdateRecord": json_path / "update",
        "CDSForm": json_path / "CDS",
        "CDSRecord": json_path / "CDS",
        "Date": json_path / "dates.json",
    }
