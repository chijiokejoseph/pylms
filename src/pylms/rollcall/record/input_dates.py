from pylms.cli.select_class_date import select_class_date
from pylms.errors import Result
from pylms.rollcall.record.dates_filter import filter_dates
from pylms.constants import DATE_FMT
from pylms.history import History


def input_class_date(history: History) -> Result[list[str]]:
    msg: str = "Attendance Marking initiated. \nPlease enter the date(s) for which attendance should be marked if available"
    src_dates: list[str] = [
        date.strftime(DATE_FMT) for date in history.get_unmarked_classes()
    ]
    result = select_class_date(msg, src_dates_list=src_dates)
    if result.is_err():
        return Result[list[str]].err(result.unwrap_err())
    chosen_dates: list[str] = result.unwrap()
    return Result[list[str]].ok(filter_dates(chosen_dates))
