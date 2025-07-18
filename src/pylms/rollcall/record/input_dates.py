from pylms.cli.select_class_date import select_class_date
from pylms.rollcall.record.dates_filter import filter_dates


def input_class_date() -> list[str]:
    msg: str = "Attendance Marking initiated. \nPlease enter the date(s) for which attendance should be marked if available"
    chosen_dates: list[str] = select_class_date(msg)
    return filter_dates(chosen_dates)
