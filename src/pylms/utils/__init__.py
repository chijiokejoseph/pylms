from pylms.utils import paths, data, date
from pylms.utils.data import DataStore, DataStream, read_csv, read_data
from pylms.utils.print_fns import print_stream
from pylms.utils.rm import rm_path
from pylms.utils.env import must_get_env


def prepare_paths() -> None:
    paths.get_json_path().mkdir(parents=True, exist_ok=True)
    paths.get_excel_path().mkdir(parents=True, exist_ok=True)
    paths.get_paths_weeks().mkdir(parents=True, exist_ok=True)
    paths.get_paths_json()["Records"].mkdir(parents=True, exist_ok=True)
    paths.get_paths_json()["Classes"].mkdir(parents=True, exist_ok=True)
    paths.get_paths_json()["Update"].mkdir(parents=True, exist_ok=True)
    paths.get_paths_json()["CDS"].mkdir(parents=True, exist_ok=True)


__all__ = [
    "data",
    "date",
    "paths",
    "prepare_paths",
    "print_stream",
    "must_get_env",
    "read_csv",
    "read_data",
    "rm_path",
    "DataStore",
    "DataStream",
]
