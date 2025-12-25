from ..errors import Result, eprint
from ..history import retrieve_dates
from .class_dates import parse_class_dates
from .class_nums import parse_class_nums
from .class_verify import verify_class


def match_date_by_index(num_input: int, dates: list[str] | None = None) -> Result[str]:
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
    class_dates = retrieve_dates("")
    if class_dates.is_err():
        return class_dates.propagate()

    dates = class_dates.unwrap() if dates is None else dates

    # Check if the input number is a valid index
    if len(dates) >= num_input > 0:
        value = dates[num_input - 1]
        return Result.ok(value)
    else:
        # If the input number is not a valid index, raise an `InvalidSelectionInputError`
        msg = f"Entered number {num_input} is not a valid option from the displayed menu. \nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)


def match_date_by_value(str_input: str) -> Result[str]:
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
    dates = retrieve_dates("")
    if dates.is_err():
        return dates.propagate()

    dates = dates.unwrap()

    # formatted string of class dates created for use for printing to the terminal
    dates_print: str = "\n"
    for date_string in dates:
        dates_print += f"{date_string}\n"

    # check if the input string is a valid date
    if str_input in dates:
        return Result.ok(str_input)
    else:
        # If the input string is not a valid date, print a warning and exit the program
        msg = f"Entered date {str_input} is not a member of {dates_print}. \nPlease try again"
        eprint(msg)
        return Result.ok(msg)


def parse_classes(entry: str, src: list[str] | None = None) -> Result[list[str]]:
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
        entry (str): User input representing date selections.

    Returns:
        Result[list[str]]: Ok with the list of selected date strings, or Err
            with a diagnostic message on failure.
    """
    # Remove leading/trailing whitespace and convert to lowercase
    entry = entry.strip().lower()

    # Retrieve the list of valid class dates
    all_dates = retrieve_dates("")
    if all_dates.is_err():
        return all_dates.propagate()

    all_dates = all_dates.unwrap()
    all_dates.append("all")

    if src is None:
        src = all_dates

    if "all" in src and src.index("all") != len(src) - 1:
        src.remove("all")
        src.append("all")

    src_set = set(src)
    all_set = set(all_dates)
    bad_dates = src_set.difference(all_set)

    if len(bad_dates) > 0:
        bad_dates = list(sorted(bad_dates))
        strings_src = f"[{', '.join(bad_dates)}]"
        strings_all = f"[{', '.join(all_dates)}]"
        msg = f"Some Dates provided in function input: {strings_src} are not in {strings_all}"
        eprint(msg)
        raise Result.fail(msg)

    # Validate the input format
    if not verify_class(entry):
        msg = f"input {entry} does not match any of the required formats"
        eprint(msg)
        return Result.err(msg).unwrap()

    # Parse input to get list of date numbers
    choice_nums = parse_class_nums(entry)
    if choice_nums.is_err():
        return choice_nums.propagate()

    choice_nums = choice_nums.unwrap()

    # Parse input to get list of date strings
    choice_dates: list[str] = parse_class_dates(entry)

    # Match input against possible cases
    match entry:
        # If input is "all", return all dates
        case _ if entry == "all" or entry == f"{len(src)}":
            src.remove("all")
            return Result.ok(src.copy())

        # If input contains valid date numbers, return corresponding dates
        case _ if len(choice_nums) > 0:
            values: list[str] = []
            for num in choice_nums:
                value = match_date_by_index(num, src)
                if value.is_err():
                    return value.propagate()
                value = value.unwrap()
                values.append(value)

            return Result.ok(values)

        # If input contains valid date strings, return corresponding dates
        case _ if len(choice_dates) > 0:
            values = []
            for date in choice_dates:
                value = match_date_by_value(date)
                if value.is_err():
                    return value.propagate()
                value = value.unwrap()
                values.append(value)

            return Result.ok(values)

        # If no match, raise error
        case _:
            msg = f"input {entry} does not match any of the required formats"
            eprint(msg)
            return Result.err(msg)
