from enum import IntEnum

from ..cli import input_option
from ..errors import Result
from ..info import print_info


class Select(IntEnum):
    """Enumeration for result edit selection types.
    
    Defines the different ways to edit student results.
    """
    ALL = 0
    BATCH = 1
    MULTIPLE = 2


def input_select_type() -> Result[Select]:
    """Prompt user to select type of result editing operation.
    
    Presents options for editing all students, multiple students individually,
    or multiple students with same adjustment.
    
    Returns:
        Result[Select]: Success with selected edit type or error.
    """
    options = [
        "Edit all students' result",
        "Edit mutliple students' result, one result at a time",
        "Edit multiple students' result with the same edit for all",
    ]
    result = input_option(options, prompt="Select a batch result edit operation")
    if result.is_err():
        return result.propagate()
    idx, choice = result.unwrap()
    print_info(f"You have selected: {choice}\n")
    match idx:
        case 1:
            return Result.ok(Select.ALL)
        case 2:
            return Result.ok(Select.MULTIPLE)
        case _:
            return Result.ok(Select.BATCH)
