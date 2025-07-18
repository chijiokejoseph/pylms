import json
from typing import cast
from io import TextIOWrapper
from pylms.utils.paths.path_fns import get_paths_json


def _save_dates(class_dates: list[str]) -> None:
    with open(get_paths_json()["Date"], mode="w") as file:
        file = cast(TextIOWrapper, file)
        json.dump(class_dates, file, indent=2)
