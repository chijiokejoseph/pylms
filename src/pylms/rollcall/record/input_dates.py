from pylms.cli.select_class_date import select_class_date
from pylms.rollcall.record.dates_filter import filter_dates
from pylms.constants import DATE_FMT
from pylms.history import History


def input_class_date(history: History) -> list[str]:
    msg: str = "Attendance Marking initiated. \nPlease enter the date(s) for which attendance should be marked if available"
    src_dates: list[str] = [
        date.strftime(DATE_FMT) for date in history.get_unmarked_classes()
    ]
    chosen_dates: list[str] = select_class_date(msg, src_dates_list=src_dates)
    return filter_dates(chosen_dates)
