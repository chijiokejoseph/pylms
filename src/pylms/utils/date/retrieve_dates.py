from typing import Literal
from pathlib import Path
import json
import sys

from pylms.utils.paths.path_fns import get_paths_json


def retrieve_dates(class_num: int | Literal["all"] = "all") -> list[str]:
    
    dates_path: Path = get_paths_json()["Date"]
    with dates_path.open(mode="r") as json_file:
        dates: list[str] = json.load(json_file)

    if isinstance(class_num, str) and class_num == "all":
        return dates
    elif class_num > 0 and class_num > len(dates):
        sys.exit(
            f"Cannot retrieve any class_date for class number {class_num}. \nThe number of scheduled classes based on initial preprocessing is {len(dates)}. If this is not the case consider reprocessing again."
        )
    elif class_num <= 0:
        sys.exit(
            "Class Numbers are expected to be positive numbers. \nThe class number input is not a list index to start from 0 or to include non-negative indices, but starts its count from 1."
        )
    else:
        return [dates[class_num - 1]]
