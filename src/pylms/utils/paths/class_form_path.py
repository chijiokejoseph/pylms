from pathlib import Path
from pylms.utils.date.retrieve_dates import retrieve_dates
from pylms.utils.date.errors import InvalidDateError
from typing import Literal

from pylms.utils.paths.path_fns import get_paths_json


def get_class_path(input_date: str, kind: Literal["class", "record"]) -> Path:
    dates_list: list[str] = retrieve_dates()
    if input_date not in dates_list:
        raise InvalidDateError(
            f"Date: {input_date} passed to function call `date.extract_path_by_date()` is not a valid class date."
        )
    class_num: int = dates_list.index(input_date) + 1
    match str(kind):
        case "class":
            key: Literal["Classes", "Records"] = "Classes"
        case _:
            key = "Records"
    return get_paths_json()[key] / f"{kind}{class_num}.json"
