from enum import Enum, auto

from ..cli import input_option
from ..errors import Result


class EditType(Enum):
    ALL = auto()
    BATCH = auto()
    MULTIPLE = auto()


def input_edit_type() -> Result[EditType]:
    options: list[str] = [
        "Edit all students attendance",
        "Edit multiple students' attendance, each record at a time",
        "Edit multiple students' attendance, with the same record for all",
    ]
    result = input_option(options, prompt="Select a batch attendance operation")

    if result.is_err():
        return result.propagate()

    choice, option = result.unwrap()
    print(f"You have selected: {option}\n")
    match int(choice):
        case 1:
            return Result.ok(EditType.ALL)
        case 2:
            return Result.ok(EditType.MULTIPLE)
        case _:
            return Result.ok(EditType.BATCH)
