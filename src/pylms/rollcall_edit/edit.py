from datetime import datetime

from ..constants import TIMESTAMP_FMT
from ..data import DataStore
from ..errors import Result, Unit
from ..history import (
    History,
    add_class_form,
    add_held_class,
    add_marked_class,
    get_unmarked_classes,
)
from ..models import ClassFormInfo
from .edit_all import edit_all_records
from .edit_multiple import edit_multiple_records
from .edit_single import edit_single_record
from .edit_type import EditType, input_edit_type
from .input_dates import input_date_for_edit


def edit_record(ds: DataStore, history: History) -> Result[Unit]:
    edit_type = input_edit_type()
    if edit_type.is_err():
        return edit_type.propagate()

    edit_type = edit_type.unwrap()

    edit_dates = input_date_for_edit(history)
    if edit_dates.is_err():
        return edit_dates.propagate()

    edit_dates = edit_dates.unwrap()

    match edit_type:
        case EditType.ALL:
            result = edit_all_records(ds, history, edit_dates)
            if result.is_err():
                return result.propagate()

        case EditType.MULTIPLE:
            result = edit_multiple_records(ds, history, edit_dates)
            if result.is_err():
                return result.propagate()

        case EditType.SINGLE:
            result = edit_single_record(ds, history, edit_dates)
            if result.is_err():
                return result.propagate()

    unmarked_dates = get_unmarked_classes(history, "")
    edited_dates_to_mark = [date for date in edit_dates if date in unmarked_dates]

    data = ds.as_ref()

    for date in edited_dates_to_mark:
        data[date] = data[date].astype(str)
        data.loc[:, date] = data[date].replace("nan", "Absent")  # pyright: ignore[reportUnknownMemberType]

        result = add_held_class(history, date)
        if result.is_err():
            return result.propagate()

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
