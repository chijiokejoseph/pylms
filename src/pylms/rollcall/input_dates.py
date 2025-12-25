from ..cli import select_class_date
from ..errors import Result, eprint
from ..history import History, get_unrecorded_classes
from .dates_filter import filter_dates


def input_class_date(history: History) -> Result[list[str]]:
    msg: str = "Attendance Marking initiated. \nPlease enter the date(s) for which attendance should be marked if available"
    dates = [date for date in get_unrecorded_classes(history, "")]
    if len(dates) == 0:
        msg = "no unmarked classes present, all classes marked"
        eprint(msg)
        return Result.err(msg)

    result = select_class_date(msg, dates_in=dates)

    if result.is_err():
        return result.propagate()

    chosen_dates = result.unwrap()
    dates = filter_dates(chosen_dates)
    if dates.is_err():
        return dates.propagate()

    dates = dates.unwrap()
    return Result.ok(dates)
