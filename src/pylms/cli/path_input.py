from pathlib import Path
from typing import Callable

from pylms.cli.custom_inputs import input_str
from pylms.cli.errors import InvalidPathError


def input_path(
    msg: str,
    str_test_fn: Callable[[str], bool] = lambda x: True,
    path_test_fn: Callable[[Path], bool] = lambda x: True,
    str_test_diagnosis: str | None = None,
    path_test_diagnosis: str | None = None,
    trials: int = 3,
) -> Path:
    path_str = input_str(msg, str_test_fn, str_test_diagnosis, trials, lower_case=False)
    path_str = path_str.strip()
    path_str = path_str.removesuffix('"')
    path_str = path_str.removesuffix("'")
    path_str = path_str.removeprefix('"')
    path_str = path_str.removeprefix("'")
    path: Path = Path(path_str)
    if not path_test_fn(path):
        diagnosis = (
            f"\nInput Path: '{path}', diagnosis: {path_test_diagnosis}"
            if path_test_diagnosis is not None
            else ""
        )
        err_msg: str = f"'{path_str}' does not meet input requirements. {diagnosis}"
        raise InvalidPathError(err_msg)
    return path


def test_path_in(path_input: Path) -> bool:
    if not path_input.is_absolute():
        print(f"{path_input} is not absolute")
        return False
    if not path_input.name.endswith("xlsx"):
        print(f"{path_input} does not point to an excel file")
        return False
    return path_input.exists()
