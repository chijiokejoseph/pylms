from datetime import datetime

from ..constants import TIMESTAMP_FMT
from ..data import DataStore
from ..errors import Result
from ..history import History
from ..models import ClassFormInfo
from .edit_all import edit_all_records
from .edit_multiple import edit_multiple_records
from .edit_single import edit_single_record
from .edit_type import EditType, input_edit_type
from .input_dates import input_date_for_edit


def edit_record(ds: DataStore, history: History) -> Result[tuple[EditType, list[str]]]:
    edit_type = input_edit_type()
    if edit_type.is_err():
        return edit_type.propagate()

    edit_type = edit_type.unwrap()

    edit_dates = input_date_for_edit(history, edit_type)
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

    return Result.ok((edit_type, edit_dates))


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
