from datetime import datetime

from ..constants import TIMESTAMP_FMT
from ..data import DataStore
from ..errors import Result, Unit
from ..history import (
    History,
    add_class_form,
    add_held_class,
    add_marked_class,
    get_unheld_classes,
    get_unmarked_classes,
)
from ..models import ClassFormInfo
from .edit_all import edit_all_records
from .edit_multiple import edit_multiple_records
from .edit_single import edit_single_record
from .edit_type import EditType, input_edit_type
from .input_dates import input_date_for_edit


def edit_record(ds: DataStore, history: History) -> Result[Unit]:
    # Select the type of edit to perform
    edit_type = input_edit_type()
    if edit_type.is_err():
        return edit_type.propagate()

    edit_type = edit_type.unwrap()

    # Get class dates to edit
    edit_dates = input_date_for_edit(history)
    if edit_dates.is_err():
        return edit_dates.propagate()

    edit_dates = edit_dates.unwrap()

    # Perform edit operation corresponding to edit type
    match edit_type:
        case EditType.ALL:
            result = edit_all_records(ds, history, edit_dates)

        case EditType.MULTIPLE:
            result = edit_multiple_records(ds, history, edit_dates)

        case EditType.SINGLE:
            result = edit_single_record(ds, history, edit_dates)

    # If the edit was unsuccessful, propagate error to caller
    if result.is_err():
        return result.propagate()

    data = ds.as_ref()

    # Cast Column data for each date to str
    for date in edit_dates:
        data[date] = data[date].astype(str).replace("nan", "")

    # If editing all records, also update history to mark classes as held and marked
    if edit_type != EditType.ALL:
        return Result.unit()

    unheld_dates = get_unheld_classes(history, "")
    unmarked_dates = get_unmarked_classes(history, "")
    unmarked_edit_dates = [date for date in edit_dates if date in unmarked_dates]
    unheld_edit_dates = [date for date in edit_dates if date in unheld_dates]

    for date in unheld_edit_dates:
        result = add_held_class(history, date)
        if result.is_err():
            return result.propagate()

    for date in unmarked_edit_dates:
        result = add_marked_class(history, date)
        if result.is_err():
            return result.propagate()

        form_info = new_edit_info(date)
        add_class_form(history, form_info)

    return Result.unit()


def new_edit_info(class_date: str) -> ClassFormInfo:
    name: str = f"Manual Attendance Entry for {class_date}"
    return ClassFormInfo(
        date=class_date,
        present_name=name,
        present_title=name,
        present_url="",
        present_id="",
        excused_name=name,
        excused_title=name,
        excused_url="",
        excused_id="",
        timestamp=datetime.now().strftime(TIMESTAMP_FMT),
    )
