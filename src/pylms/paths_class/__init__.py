from pathlib import Path
from typing import Literal

from ..errors import Result, eprint
from ..history import all_dates, load_history
from ..paths import get_paths_json


def get_class_path(input_date: str, kind: Literal["class", "record"]) -> Result[Path]:
    history = load_history()
    if history.is_err():
        return history.propagate()

    history = history.unwrap()
    dates = all_dates(history, "")
    if input_date not in dates:
        msg = f"Date: {input_date} passed to function call `date.extract_path_by_date()` is not a valid class date."
        eprint(msg)
        return Result.err(msg)
    class_num: int = dates.index(input_date) + 1
    match kind:
        case "class":
            key: Literal["Classes", "Records"] = "Classes"
        case _:
            key = "Records"
    value = get_paths_json()[key] / f"{kind}{class_num}.json"
    return Result.ok(value)
