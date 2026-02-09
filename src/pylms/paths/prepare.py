from .path_fns import get_excel_path


def prepare_paths() -> None:
    get_excel_path().mkdir(parents=True, exist_ok=True)
