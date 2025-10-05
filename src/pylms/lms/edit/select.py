from enum import IntEnum

from pylms.cli import input_option
from pylms.errors import Result


class Select(IntEnum):
    ALL = 0
    BATCH = 1
    MULTIPLE = 2


def input_select_type() -> Result[Select]:
    options: list[str] = [
        "Edit all students' result",
        "Edit mutliple students' result, one result at a time",
        "Edit multiple students' result with the same edit for all",
    ]
    result = input_option(options, prompt="Select a batch result edit operation")
    if result.is_err():
        return Result[Select].err(result.unwrap_err())
    idx, choice = result.unwrap()
    print(f"You have selected: {choice}\n")
    match idx:
        case 1:
            return Result[Select].ok(Select.ALL)
        case 2:
            return Result[Select].ok(Select.MULTIPLE)
        case _:
            return Result[Select].ok(Select.BATCH)
