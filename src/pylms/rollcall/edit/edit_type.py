from enum import Enum, auto
from pylms.cli import input_option
from pylms.errors import Result


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
        return Result[EditType].err(result.unwrap_err())
    choice, option = result.unwrap()
    print(f"You have selected: {option}\n")
    match int(choice):
        case 1:
            return Result[EditType].ok(EditType.ALL)
        case 2:
            return Result[EditType].ok(EditType.MULTIPLE)
        case _:
            return Result[EditType].ok(EditType.BATCH)
