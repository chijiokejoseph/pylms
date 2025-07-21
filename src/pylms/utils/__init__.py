from pylms.utils import paths, clean, clean_special, data, date, grade
from pylms.utils.data import DataStore, DataStream, read_csv, read_data
from pylms.utils.print_fns import print_stream
from pylms.utils.rm import rm_path


def prepare_paths() -> None:
    paths.get_json_path().mkdir(parents=True, exist_ok=True)
    paths.get_excel_path().mkdir(parents=True, exist_ok=True)
    paths.get_paths_weeks().mkdir(parents=True, exist_ok=True)
    paths.get_paths_json()["Records"].mkdir(parents=True, exist_ok=True)
    paths.get_paths_json()["Classes"].mkdir(parents=True, exist_ok=True)
    paths.get_paths_json()["Update"].mkdir(parents=True, exist_ok=True)
    paths.get_paths_json()["CDS"].mkdir(parents=True, exist_ok=True)


__all__ = [
    "clean",
    "clean_special",
    "data",
    "date",
    "grade",
    "paths",
    "prepare_paths",
    "print_stream",
    "read_csv",
    "read_data",
    "rm_path",
    "DataStore",
    "DataStream",
]
