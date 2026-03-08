from ..cli import input_bool
from ..config import Config
from ..data import DataStore
from ..errors import Result, Unit
from ..history import (
    History,
    get_class_info,
    get_date_index,
    get_held_classes,
    get_marked_classes,
)
from ..info import print_info
from ..query_dates import search_unheld
from .class_form_init import init_class_form


def request_class_form(config: Config, ds: DataStore, history: History) -> Result[Unit]:
    """Request creation of class forms for selected dates.

    Allows user to select dates and handles existing forms by showing current
    URLs and asking if regeneration is needed. Only creates new forms for
    dates that need them.

    Args:
        config: Config containing facilitator information.
        ds: DataStore containing student data.
        history: History object for tracking operations.

    Returns:
        Result[Unit]: Success or error message.
    """
    # Request dates from user
    dates = search_unheld(history)
    if dates.is_err():
        return dates.propagate()

    dates = dates.unwrap()
    print(f"You have selected the following dates: {dates}")

    new_dates: list[str] = dates.copy()

    # Check each date for existing forms
    for date in dates:
        class_num = get_date_index(history, date).unwrap()

        if date not in get_held_classes(history, ""):
            continue

        info = get_class_info(history, date)
        if info.is_err():
            continue

        info = info.unwrap()
        print_info(f"\nClass {class_num} held on Date: {date}")
        print_info(f"Attendance Url: {info.present_url}")
        print_info(f"Excused Url: {info.excused_url}\n")

        # Check if attendance already recorded
        marked_dates = get_marked_classes(history, "")
        if date in marked_dates:
            print_info(f"Attendance for Class {class_num} has been recorded")
            continue

        # Ask if user wants to regenerate form
        choice = input_bool(
            f"Do you wish to regenerate the attendance for Class {class_num}: "
        )
        if choice.is_err():
            return choice.propagate()

        choice = choice.unwrap()

        if not choice:
            continue

        new_dates.remove(date)

    # Create forms for new dates only
    if len(new_dates) == 0:
        return Result.unit()
    return init_class_form(config, ds, history, new_dates)
