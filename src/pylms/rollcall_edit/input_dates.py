from datetime import datetime

from ..cli import select_class_date
from ..constants import DATE_FMT
from ..errors import Result
from ..history import History
from .edit_type import EditType


def input_date_for_edit(history: History, edit_type: EditType) -> Result[list[str]]:
    msg: str = "Manual Attendance Marking initiated. \nPlease enter the date(s) for which attendance should be marked if available"

    def to_str(dates: list[datetime]) -> list[str]:
        return [date.strftime(DATE_FMT) for date in dates]

    match edit_type:
        case EditType.ALL:
            src_dates: list[str] = to_str(history.dates)
        case _:
            src_dates = to_str(history.marked_classes)

    return select_class_date(msg, dates_in=src_dates)
