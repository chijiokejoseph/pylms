from ..cli_utils import parse_class_dates, parse_nums, verify_class
from ..constants import COMMA_DELIM
from ..errors import Result, eprint
from .dates_with_history import all_dates
from .history import History


def match_date_by_index(
    history: History, date_index: int, dates: list[str] | None = None
) -> Result[str]:
    """Return the class date string for a 1-based index.

    Retrieves the list of class dates and returns the date string at the
    provided 1-based index. If the index is out of range this function
    returns an error `Result` describing the invalid selection.

    Args:
        num_input (int): 1-based index of the desired date.
        dates (list[str] | None): a dates src list to match the 1-based
            index against. If None, defaults to all the class dates

    Returns:
        Result[str]: Ok containing the date string when the index is valid,
            or Err with a diagnostic message when the index is invalid.
    """
    # Retrieve the list of class dates
    class_dates = all_dates(history, "")
    dates = class_dates if dates is None else dates

    # Check if the input number is a valid index
    if len(dates) >= date_index > 0:
        value = dates[date_index - 1]
        return Result.ok(value)
    else:
        # If the input number is not a valid index, raise an `InvalidSelectionInputError`
        msg = f"Entered number {date_index} is not a valid option from the displayed menu. \nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)


def match_date_by_value(history: History, date: str) -> Result[str]:
    """Validate that the input date string is one of the class dates.

    Checks whether `str_input` (expected in the format 'dd/mm/yyyy') is
    present in the list of available class dates. If present the same date
    string is returned inside `Result.ok`; otherwise an error `Result` with
    a diagnostic message is returned.

    Args:
        str_input (str): Date string to validate (format 'dd/mm/yyyy').

    Returns:
        Result[str]: Ok containing the validated date string, or Err with a
            diagnostic message when the date is not available.
    """

    # get class dates
    dates = all_dates(history, "")

    # formatted string of class dates created for use for printing to the terminal
    dates_print: str = "\n"
    for date_string in dates:
        dates_print += f"{date_string}\n"

    # check if the input string is a valid date
    if date in dates:
        return Result.ok(date)
    else:
        # If the input string is not a valid date, print a warning and exit the program
        msg = (
            f"Entered date {date} is not a member of {dates_print}. \nPlease try again"
        )
        eprint(msg)
        return Result.ok(msg)


def match_classes(
    history: History, class_input: str, src: list[str] | None = None
) -> Result[list[str]]:
    """Parse user input into a list of class date strings.

    Accepts several input formats:
    - One or more 1-based indices (numbers) separated by commas, which are
      mapped to class dates.
    - One or more date strings in 'dd/mm/yyyy' format separated by commas.
    - The special token 'all' is handled by callers of this function.

    The function validates the input format, resolves numeric selections to
    date strings, and returns the selected date strings wrapped in a
    `Result.ok`. If the input is invalid or references unavailable dates, a
    `Result.err` with a diagnostic message is returned.

    Args:
        class_input (str): User input representing date selections.

    Returns:
        Result[list[str]]: Ok with the list of selected date strings, or Err
            with a diagnostic message on failure.
    """
    # Remove leading/trailing whitespace and convert to lowercase
    class_input = class_input.strip().lower()

    # Retrieve the list of valid class dates
    classes = all_dates(history, "")
    classes.append("all")

    if src is None:
        src = classes

    if "all" in src and src.index("all") != len(src) - 1:
        src.remove("all")
        src.append("all")

    src_set = set(src)
    classes_set = set(classes)
    bad_dates = src_set.difference(classes_set)

    if len(bad_dates) > 0:
        bad_dates = list(sorted(bad_dates))
        strings_src = f"[{COMMA_DELIM.join(bad_dates)}]"
        strings_all = f"[{COMMA_DELIM.join(classes)}]"
        msg = f"Some Dates provided in function input: {strings_src} are not in {strings_all}"
        eprint(msg)
        raise Result.fail(msg)

    # Validate the input format
    if not verify_class(class_input):
        msg = f"input {class_input} does not match any of the required formats"
        eprint(msg)
        return Result.err(msg).unwrap()

    # Parse input to get list of date numbers
    input_class_nums = parse_nums(class_input)
    if input_class_nums.is_err():
        return input_class_nums.propagate()

    input_class_nums = input_class_nums.unwrap()

    # Parse input to get list of date strings
    input_class_dates: list[str] = parse_class_dates(class_input)

    # Match input against possible cases
    match class_input:
        # If input is "all", return all dates
        case _ if class_input == "all" or class_input == f"{len(src)}":
            src.remove("all")
            return Result.ok(src.copy())

        # If input contains valid date numbers, return corresponding dates
        case _ if len(input_class_nums) > 0:
            values: list[str] = []
            for num in input_class_nums:
                value = match_date_by_index(history, num, src)
                if value.is_err():
                    return value.propagate()
                value = value.unwrap()
                values.append(value)

            return Result.ok(values)

        # If input contains valid date strings, return corresponding dates
        case _ if len(input_class_dates) > 0:
            values = []
            for date in input_class_dates:
                value = match_date_by_value(history, date)
                if value.is_err():
                    return value.propagate()
                value = value.unwrap()
                values.append(value)

            return Result.ok(values)

        # If no match, raise error
        case _:
            msg = f"input {class_input} does not match any of the required formats"
            eprint(msg)
            return Result.err(msg)
