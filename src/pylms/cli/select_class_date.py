from ..cli_utils import parse_to_dates, val_date_str
from ..errors import Result
from ..history import retrieve_dates
from ..info import print_info
from .custom_inputs import input_str


def select_class_date(msg: str, dates_in: list[str] | None = None) -> Result[list[str]]:
    """Prompt the user to select one or more class dates.

    Presents instructions and a numbered menu of available class dates, then
    prompts the user for a selection. Accepted input formats include:
    - Single index (e.g. "1")
    - Exact date (e.g. "13/01/2025")
    - Comma-separated indices (e.g. "1, 2, 3")
    - Comma-separated dates (e.g. "13/01/2025, 14/01/2025")
    - Ranges of indices (e.g. "1-3", "1, 3-5")
    - The token "all" to select every available date

    The function validates the user's input, resolves indices to date
    strings, and returns the selected dates inside a `Result.ok`. Errors from
    the interactive helpers are propagated as `Result.err`.

    Args:
        msg (str): Message printed before displaying the date menu.
        dates_in (list[str] | None): Optional list of candidate date strings to
            present. When `None` the stored class dates are used.

    Returns:
        Result[list[str]]: Ok with the list of selected date strings on
            success, or an Err with a diagnostic message when parsing or
            validation fails.

    Example:
        >>> select_class_date(\"Choose class date:\")
        Result.ok(['13/01/2025'])
    """

    # get class dates
    all_dates = retrieve_dates("")
    if all_dates.is_err():
        return all_dates.propagate()

    all_dates = all_dates.unwrap()
    dates_list: list[str] = dates_in if dates_in is not None else all_dates
    if dates_in is None:
        dates_list.append(
            "all"
        )  # add all to add an option for selecting all the class_dates at once
    print(msg)
    guide: str = f"""
You can enter dates in the following formats:
    - Single class number (e.g. "1")
    - Exact date (e.g. "13/01/2025")
    - Comma-separated class numbers (e.g. "1, 2, 3")
    - Comma-separated exact dates (e.g. "13/01/2025, 14/01/2025")
    - Date ranges (e.g. "1 - 3", "1 -3, 5, 7 - 10")
    - "{len(dates_list)}" or "all" to select all available dates
Note: Dates must match the menu displayed above.
    """
    # prints out the instructions on how to select class dates
    print_info(guide)

    print_info("The class dates with their class numbers are printed below")
    # print out each class date and an option number for each class date
    for each_date in dates_list:
        i: int = (
            all_dates.index(each_date) + 1 if each_date != "all" else len(all_dates) + 1
        )
        print(f"Class {i}. {each_date}")

    # uses `input_str` and the validation function `_date_val_input` to validate user input
    result = input_str(
        "Enter the relevant date(s): ",
        val_date_str,
        diagnosis="Your input is invalid. Please confirm that your response matches any of the constraints stated above.",
    )
    if result.is_err():
        return result.propagate()
    response: str = result.unwrap()
    # parses the user input with the function _parse_date
    class_dates = parse_to_dates(response)
    if class_dates.is_err():
        return class_dates.propagate()

    class_dates = class_dates.unwrap()

    print_info(f"You have selected {class_dates}\n")
    return Result.ok(class_dates)
