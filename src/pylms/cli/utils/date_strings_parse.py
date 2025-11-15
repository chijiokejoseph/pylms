from pylms.cli.utils.date_str_parse import _parse_date_str
from pylms.cli.utils.date_strings_verify import val_date_str
from pylms.cli.utils.int_str_parse import _parse_int_str
from pylms.errors import LMSError
from pylms.utils.date.retrieve_dates import retrieve_dates


def match_date_by_index(num_input: int) -> str:
    """
    This function takes in an integer `num_input` and returns the date string corresponding to that number from the list of class dates.
    If the number is not a valid index (i.e., less than 1 or greater than the length of the list), it raises an `InvalidSelectionInputError`.

    :param num_input: An integer representing the index of the date to retrieve.
    :type num_input: int

    :return: The date string corresponding to the given index.
    :rtype: str

    :raises InvalidSelectionInputError: If the input number is not a valid index for the list of class dates.
    """
    # Retrieve the list of class dates
    dates_list: list[str] = retrieve_dates()
    # Check if the input number is a valid index
    if len(dates_list) >= num_input > 0:
        return dates_list[num_input - 1]
    else:
        # If the input number is not a valid index, raise an `InvalidSelectionInputError`
        raise LMSError(
            f"Entered number {num_input} is not a valid option from the displayed menu. \nPlease restart the program and try again."
        )


def match_date_by_value(str_input: str) -> str:
    """
    this function takes in a string as argument to `str_input`. The string passed to this function is obtained directly from the user and is validated using regular expressions to match the format **dd/mm/yyyy** which is used in the class dates stored in the variable from outer scope `dates_list`.

    This function's main role is to check if this validated string passed in as input to the function is actually a member of the available date strings in `dates_list`. If true, the string is returned else the program is forced to exit with a warning.

    :param str_input: A string that has been validated with regular expressions to match the form **dd/mm/yyyy**
    :type str_input: str

    :return: a valid date that is a member of the class dates stored in `dates_list`
    :rtype: str
    """

    # get class dates
    dates_list: list[str] = retrieve_dates()

    # formatted string of class dates created for use for printing to the terminal
    dates_print: str = "\n"
    for date_string in dates_list:
        dates_print += f"{date_string}\n"

    # check if the input string is a valid date
    if str_input in dates_list:
        return str_input
    else:
        # If the input string is not a valid date, print a warning and exit the program
        raise LMSError(
            f"Entered date {str_input} is not a member of {dates_print}. \nPlease restart the program and try again"
        )


def parse_to_dates(entry: str) -> list[str]:
    """
    A helper function that parses a string entered by a user and returns a list of corresponding date strings.
    The string entered by the user is designed to match one of the following formats:

    - case `entry` = "d" / "dd" e.g., "1" or "12":
        The `entry` is converted to an int and then converted to an index for the list of class dates.
        Upon indexing this list, the obtained date is returned as a list containing a single date string.
        If the indexing conditions are not met, the program is forcefully exited.

    - case `entry` = "d, dd" e.g., "1, 12" or "12, 1":
        The `entry` is split into substrings using "," after which each substring is trimmed of its whitespaces,
        converted to an int and parsed using the same formula for the previous case.
        If each individual substring is parsed successfully, their corresponding dates are returned as a `list[str]`.

    - case `entry` = "dd/mm/yyyy" e.g., "12/01/2025":
        The `entry` is just checked to be a member of the list of class dates before being returned.
        If it is not, the program is forcefully exited.

    - case `entry` = "dd/mm/yyyy, dd/mm/yyyy" e.g., "12/01/2025, 13/01/2025":
        The `entry` is split into substrings using "," after which each substring is trimmed of its whitespaces,
        and then parsed individually using the same formula for the previous case.
        If each individual substring is parsed successfully, their corresponding dates are returned as a `list[str]`.

    Should no case be matched, the program is forcefully exited.

    :param entry: (str) - A user input string representing class date selections.
    :type entry: str

    :return: (list[str]) - List of valid class dates as strings.
    :rtype: list[str]

    :raises InvalidSelectionInputError: If the input does not match any required formats or valid dates.
    """
    # Remove leading/trailing whitespace and convert to lowercase
    entry = entry.strip().lower()

    # Retrieve the list of valid class dates
    dates_list: list[str] = retrieve_dates()

    # Validate the input format
    if not val_date_str(entry):
        raise LMSError(f"input {entry} does not match any of the required formats")

    # Parse input to get list of date numbers
    choice_nums: list[int] = _parse_int_str(entry)
    # Parse input to get list of date strings
    choice_dates: list[str] = _parse_date_str(entry)

    # Match input against possible cases
    match entry:
        # If input is "all", return all dates
        case "all":
            return dates_list.copy()

        # If input contains valid date numbers, return corresponding dates
        case _ if len(choice_nums) > 0:
            return [match_date_by_index(num) for num in choice_nums]

        # If input contains valid date strings, return corresponding dates
        case _ if len(choice_dates) > 0:
            return [match_date_by_value(date) for date in choice_dates]

        # If no match, raise error
        case _:
            raise LMSError(f"input {entry} does not match any of the required formats")
