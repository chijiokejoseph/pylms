from typing import Callable, cast

from pylms.cli.custom_inputs import input_num
from pylms.errors import Result
from pylms.record import RecordStatus
from pylms.utils.date.retrieve_dates import retrieve_dates


def input_record(target_date: str, options: list[RecordStatus]) -> Result[RecordStatus]:
    """
    Prompt the user to select a record status for a given class date from a list of options.

    :param target_date: (str) - The date of the class for which the record status is to be set.
    :param options: (list[RecordStatus]) - A list of possible record status options.

    :return: (Result[RecordStatus]) - A result containing the selected record status.
    :rtype: Result[RecordStatus]
    """
    # Retrieve all class dates
    class_dates: list[str] = retrieve_dates()
    # Display options to the user
    print("\nSelect from the following: ")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    # Determine the class number based on the target date
    class_num: int = class_dates.index(target_date) + 1
    # Prepare the prompt message for user input
    prompt: str = f"""
From the options presented above listed {1} - {len(options)},
Please Select which of the following Record Status should be set
\nFor Class {class_num} held on {target_date} (only integers from 1 - {len(options)} are allowed):  """

    # Validation function to ensure input is within valid range
    def validate_input(entered_num: int) -> bool:
        return 1 <= entered_num <= len(options)

    validate_fn = cast(Callable[[float | int], bool], validate_input)

    # Prompt user for input with validation
    result: Result[int | float] = input_num(prompt, "int", test_fn=validate_fn)
    if result.is_err():
        return Result[RecordStatus].err(result.unwrap_err())
    selection_temp = result.unwrap()
    selection: int = cast(int, selection_temp)

    # Get the selected record status based on user input
    selected_record: RecordStatus = options[selection - 1]

    # Display the selected record status
    print(f"You have selected: {selected_record}")

    # Return the selected record status
    return Result[RecordStatus].ok(selected_record)
