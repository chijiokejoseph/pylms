from ..cli import input_option
from ..errors import Result
from ..history import History, all_dates
from ..info import print_info
from ..record import RecordStatus

RECORDS = [RecordStatus.PRESENT, RecordStatus.ABSENT, RecordStatus.EXCUSED]


def input_record(
    history: History, target_date: str, options: list[RecordStatus]
) -> Result[RecordStatus]:
    """
    Prompt the user to select a record status for a given class date from a list of options.

    :param target_date: (str) - The date of the class for which the record status is to be set.
    :param options: (list[RecordStatus]) - A list of possible record status options.

    :return: (Result[RecordStatus]) - A result containing the selected record status.
    :rtype: Result[RecordStatus]
    """
    # Retrieve all class dates
    class_dates: list[str] = all_dates(history, "")

    # Determine the class number based on the target date
    class_num: int = class_dates.index(target_date) + 1

    # Prepare the prompt message for user input
    prompt: str = f"""Please Select which of the following Record Status should be set
\nFor Class {class_num} held on {target_date}"""

    # Prompt user for input with validation
    result = input_option([str(value) for value in options], prompt)
    if result.is_err():
        return result.propagate()
    idx, _ = result.unwrap()

    # Get the selected record status based on user input
    selected_record = options[idx - 1]

    # Display the selected record status
    print_info(f"You have selected: {selected_record}")

    # Return the selected record status
    return Result.ok(selected_record)
