import json
from pathlib import Path

from pylms.forms.request_form_api.class_form_init import init_class_form
from pylms.forms.request_form_api.utils import ClassFormInfo
from pylms.forms.request_form_api.utils.class_date_input import input_class_date
from pylms.utils import DataStore, paths
from pylms.state import History


def request_class_form(ds: DataStore, history: History) -> None:
    form_dates: list[str] = input_class_date()
    print(f"You have selected the following dates: {form_dates}")

    new_form_dates: list[str] = form_dates.copy()

    for date in form_dates:
        class_num: int = form_dates.index(date) + 1
        metadata_path: Path = paths.get_class_path(date, "class")
        if metadata_path.exists():
            print(
                f"\n{date} has already had attendance and excused lists generated for it.\n"
            )
            with metadata_path.open("r", encoding="utf-8") as file:
                data: dict = json.load(file)
                info: ClassFormInfo = ClassFormInfo(**data)
                print(f"\nClass {class_num} held on Date: {date}")
                print(f"Attendance Url: {info.present_url}")
                print(f"Excused Url: {info.excused_url}\n")
                print()
            new_form_dates.remove(date)

    if len(new_form_dates) == 0:
        return None
    init_class_form(ds, history, new_form_dates)
    return None
