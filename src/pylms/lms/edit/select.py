from enum import IntEnum

from pylms.cli import input_option


class Select(IntEnum):
    ALL = 0
    BATCH = 1
    MULTIPLE = 2


def input_select_type() -> Select:
    options: list[str] = [
        "Edit all students' result",
        "Edit mutliple students' result, one result at a time",
        "Edit multiple students' result with the same edit for all",
    ]
    idx, choice = input_option(options, prompt="Select a batch result edit operation")
    print(f"You have selected: {choice}\n")
    match idx:
        case 0:
            return Select.ALL
        case 1:
            return Select.MULTIPLE
        case _:
            return Select.BATCH
