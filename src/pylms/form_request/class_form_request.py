from pylms.cli import input_bool

from ..data import DataStore
from ..errors import Result, Unit
from ..form_utils import input_class_date
from ..history import History, get_held_classes, get_marked_classes, match_date_index, match_info_by_date
from ..info import print_info
from .class_form_init import init_class_form


def request_class_form(ds: DataStore, history: History) -> Result[Unit]:
    dates = input_class_date(history)
    if dates.is_err():
        return dates.propagate()

    dates = dates.unwrap()
    print(f"You have selected the following dates: {dates}")

    new_dates: list[str] = dates.copy()

    # Remove dates that have already been previously marked from `new_dates`
    for date in dates:
        class_num = match_date_index(history, date).unwrap()

        # If date has not been previously generated skip
        if date not in get_held_classes(history, ""):
            continue

        info = match_info_by_date(history, date)
        if info.is_err():
            continue

        info = info.unwrap()
        print_info(f"\nClass {class_num} held on Date: {date}")
        print_info(f"Attendance Url: {info.present_url}")
        print_info(f"Excused Url: {info.excused_url}\n")

        marked_dates = get_marked_classes(history, "")
        # If data has been marked do not attempt to regenerate again
        if date in marked_dates:
            print_info(f"Attendance for Class {class_num} has been recorded")
            continue

        choice = input_bool(
            f"Do you wish to regenerate the attendance for Class {class_num}: "
        )
        if choice.is_err():
            return choice.propagate()

        choice = choice.unwrap()

        if not choice:
            continue

        new_dates.remove(date)

    if len(new_dates) == 0:
        return Result.unit()
    return init_class_form(ds, history, new_dates)
