from ..cli import input_bool, select_class_date
from ..errors import Result
from ..history import History, get_marked_classes, get_unmarked_classes
from .edit_type import EditType


def input_date_for_edit(history: History, edit_type: EditType) -> Result[list[str]]:
    msg: str = "Manual Attendance Marking initiated. \nPlease enter the date(s) for which attendance should be marked"

    match edit_type:
        case EditType.ALL:
            choice = input_bool(
                "Do you wish to edit a date whose attendance has already been recorded?"
            )
            if choice.is_err():
                return choice.propagate()

            choice = choice.unwrap()
            if choice:
                src_dates = get_marked_classes(history, "")
            else:
                src_dates = get_unmarked_classes(history, "")
        case _:
            src_dates = get_marked_classes(history, "")

    return select_class_date(msg, dates_in=src_dates)
