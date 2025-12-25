from pylms.cli.option_input import input_bool

from ..cli_utils import parse_classes, verify_class
from ..errors import Result, eprint
from ..history import retrieve_dates
from ..info import print_info
from ..numutil import det_num_width, max_content_width, max_index_width
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
    dates: list[str] = dates_in if dates_in is not None else all_dates

    if len(dates) == 0:
        msg = "There are no dates to choose from for your selected type of dates"
        eprint(msg)
        return Result.err(msg)

    dates.append("all")

    print_info(msg)

    guide: str = f"""You can enter dates in the following formats:
    - Single class number (e.g. "1")
    - Exact date (e.g. "13/01/2025")
    - Comma-separated class numbers (e.g. "1, 2, 3")
    - Comma-separated exact dates (e.g. "13/01/2025, 14/01/2025")
    - Date ranges (e.g. "1 - 3", "1 -3, 5, 7 - 10")
    - "{len(dates)}" or "all" to select all available dates
Note: Dates must match the menu displayed above.
    """

    # prints out the instructions on how to select class dates
    print_info(guide)

    print_info("The class dates with their class numbers are printed below")

    # print out each class date and an option number for each class date
    num_width = max_index_width(dates)
    max_width = max_content_width(dates)
    class_key = f"Class {len(dates)}"
    class_key_width = det_num_width(class_key)

    for idx, each_date in enumerate(dates, start=1):
        if each_date != "all":
            class_num = all_dates.index(each_date) + 1
            class_key = f"Class {class_num}"
            print(
                f"{idx:<{num_width}} . {class_key:{class_key_width}} : {each_date:{max_width}}"
            )
        else:
            class_num = len(dates)
            class_key = ""
            print(f"{idx:<{num_width}} . {each_date:{max_width}}")

    # uses `input_str` and the validation function `_date_val_input` to validate user input
    result = input_str(
        "Enter the relevant date(s): ",
        verify_class,
        diagnosis="Your input is invalid. Please confirm that your response matches any of the constraints stated above.",
    )
    if result.is_err():
        return result.propagate()

    response: str = result.unwrap()

    # parses the user input with the function _parse_date
    class_dates = parse_classes(response, dates)
    if class_dates.is_err():
        return class_dates.propagate()

    class_dates = class_dates.unwrap()

    print_info(f"You have selected {class_dates}\n")

    choice = input_bool("Proceed with these dates?")
    if choice.is_err():
        return choice.propagate()
    choice = choice.unwrap()

    if not choice:
        msg = "You have cancelled the current operation"
        print_info(msg)
        return Result.err(msg)

    return Result.ok(class_dates)
