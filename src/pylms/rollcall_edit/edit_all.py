from ..data import DataStore
from ..errors import Result, Unit, eprint
from ..history import (
    History,
    add_held_class,
    add_marked_class,
    get_unmarked_classes,
    match_date_index,
)
from ..info import printpass
from .edit_utils import edit_all_serials


def edit_all_records(
    ds: DataStore, history: History, dates_to_mark: list[str]
) -> Result[Unit]:
    if len(dates_to_mark) == 0:
        msg = "dates_to_mark should not be empty"
        eprint(msg)
        return Result.err(msg)

    result = edit_all_serials(ds, history, dates_to_mark, "public")
    if result.is_err():
        return result.propagate()

    unmarked_dates = get_unmarked_classes(history, "")
    edited_dates = [date for date in dates_to_mark if date in unmarked_dates]

    for date in edited_dates:
        result = add_held_class(history, date)
        if result.is_err():
            return result.propagate()

        result = add_marked_class(history, date)
        if result.is_err():
            return result.propagate()

        class_num = match_date_index(history, date).unwrap()
        printpass(f"Recorded attendance for Class {class_num} held on '{date}'")

    return Result.unit()
