from .path_fns import get_excel_path, get_json_path, get_paths_json, get_paths_weeks


def prepare_paths() -> None:
    get_json_path().mkdir(parents=True, exist_ok=True)
    get_excel_path().mkdir(parents=True, exist_ok=True)
    get_paths_weeks().mkdir(parents=True, exist_ok=True)
    get_paths_json()["Records"].mkdir(parents=True, exist_ok=True)
    get_paths_json()["Classes"].mkdir(parents=True, exist_ok=True)
    get_paths_json()["Update"].mkdir(parents=True, exist_ok=True)
    get_paths_json()["CDS"].mkdir(parents=True, exist_ok=True)
