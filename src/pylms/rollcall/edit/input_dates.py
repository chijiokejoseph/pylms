from pylms.cli import select_class_date
from pylms.errors import Result
from pylms.rollcall.edit.edit_type import EditType
from pylms.history import History
from datetime import datetime
from pylms.constants import DATE_FMT


def input_date_for_edit(history: History, edit_type: EditType) -> Result[list[str]]:
    msg: str = "Manual Attendance Marking initiated. \nPlease enter the date(s) for which attendance should be marked if available"
    def to_str(dates: list[datetime]) -> list[str]:
        return [
            date.strftime(DATE_FMT) for date in dates
        ]
        
    match edit_type:
        case EditType.ALL:
            src_dates: list[str] = to_str(history.dates)
        case _:
            src_dates = to_str(history.marked_classes)
    
    return select_class_date(msg, src_dates_list=src_dates)
