from .path_fns import get_excel_path, get_json_path


def prepare_paths() -> None:
    get_json_path().mkdir(parents=True, exist_ok=True)
    get_excel_path().mkdir(parents=True, exist_ok=True)
