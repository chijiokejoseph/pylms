import json
from typing import Any

from ..data import DataStore
from ..errors import Result, Unit
from ..form_utils import input_class_date
from ..history import History
from ..info import print_info
from ..models import ClassFormInfo
from ..paths_class import get_class_path
from .class_form_init import init_class_form


def request_class_form(ds: DataStore, history: History) -> Result[Unit]:
    dates_result = input_class_date(history)
    if dates_result.is_err():
        return dates_result.propagate()

    form_dates: list[str] = dates_result.unwrap()
    print(f"You have selected the following dates: {form_dates}")

    new_form_dates: list[str] = form_dates.copy()

    for date in form_dates:
        class_num: int = form_dates.index(date) + 1
        metadata_path = get_class_path(date, "class")
        if metadata_path.is_err():
            return metadata_path.propagate()

        metadata_path = metadata_path.unwrap()

        if metadata_path.exists():
            print_info(
                f"\n{date} has already had attendance and excused lists generated for it.\n"
            )
            with metadata_path.open("r", encoding="utf-8") as file:
                data: dict[Any, Any] = json.load(file)
                info: ClassFormInfo = ClassFormInfo(**data)
                print(f"\nClass {class_num} held on Date: {date}")
                print(f"Attendance Url: {info.present_url}")
                print(f"Excused Url: {info.excused_url}\n")
                print()
            new_form_dates.remove(date)

    if len(new_form_dates) == 0:
        return Result.unit()
    return init_class_form(ds, history, new_form_dates)
