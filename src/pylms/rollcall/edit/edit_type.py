from enum import Enum, auto
from pylms.cli import input_option


class EditType(Enum):
    ALL = auto()
    BATCH = auto()
    MULTIPLE = auto()


def input_edit_type() -> EditType:
    options: list[str] = [
        "Edit all students attendance",
        "Edit multiple students' attendance, each record at a time",
        "Edit multiple students' attendance, with the same record for all",
    ]
    choice, option = input_option(options, prompt="Select a batch attendance operation")

    print(f"You have selected: {option}\n")
    match int(choice):
        case 1:
            return EditType.ALL
        case 2:
            return EditType.MULTIPLE
        case _:
            return EditType.BATCH
