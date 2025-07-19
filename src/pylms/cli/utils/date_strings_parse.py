from pylms.cli.errors import InvalidSelectionInputError
from pylms.utils.date.retrieve_dates import retrieve_dates
from pylms.cli.utils.int_str_parse import _parse_int_str
from pylms.cli.utils.date_str_parse import _parse_date_str
from pylms.cli.utils.date_strings_verify import val_date_str


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

    dates_list: list[str] = retrieve_dates()
    if len(dates_list) >= num_input > 0:
        return dates_list[num_input - 1]
    else:
        raise InvalidSelectionInputError(
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

    if str_input in dates_list:
        return str_input
    else:
        raise InvalidSelectionInputError(
            f"Entered date {str_input} is not a member of {dates_print}. \nPlease restart the program and try again"
        )


def parse_to_dates(entry: str) -> list[str]:
    """
    a private helper function that parses a string entered by a user and returns a list of corresponding date strings. The string entered by the user is designed to match one of the following formats:

    match `entry`:
        - case `entry` = "d" / "dd" e.g., "1" or "12":

            in this case the `entry` is converted to an int and then converted to an index for the list of class dates. Upon indexing this list, the obtained date is returned as a list containing a single date string. If the indexing conditions are not met, the program is forcefully exit.

        - case `entry` = "d, dd" e.g., "1, 12" or "12, 1":

            in this case the `entry` is split into sub strings using "," after which each substring is trimmed of its whitespaces, converted to an int and parsed using the same formula for the previous case. If each individual substring is parsed successfully, their corresponding dates are returned as a `list[str]`

        - case `entry` = "dd/mm/yyyy" e.g., "12/01/2025":

            in this case the `entry` is just checked to be a member of the list of class dates before being returned. If it is not, the program is forcefully exit.

        - case `entry` = "dd/mm/yyyy, dd/mm/yyyy" e.g., "12/01/2025, 13/01/2025":

            in this case the `entry` is split into sub strings using "," after which each substring is trimmed of its whitespaces, and then parsed individually using the same formula for the previous case. If each individual substring is parsed successfully, their corresponding dates are returned as a `list[str]`

        should no case be matched, the program is exit forcefully.

    :param entry: ( str ): a response from the user entered in response to a prompt giving out instructions on how to select a class date form the list of class dates stored by the program. This response is now parsed to return a list of valid class dates as strings. The matching method is explained above.
    :type entry: str

    :return: list of valid class dates as strings.
    :rtype: list[str]
    """
    # remove unnecessary spaces that affect matching `entry` with regular expressions
    entry = entry.strip().lower()

    # get class dates
    dates_list: list[str] = retrieve_dates()

    if not val_date_str(entry):
        raise InvalidSelectionInputError(
            f"input {entry} does not match any of the required formats"
        )

    choice_nums: list[int] = _parse_int_str(entry)
    choice_dates: list[str] = _parse_date_str(entry)

    match entry:
        # check for "all" input and return all dates
        case "all":
            return dates_list.copy()

        # check for valid class date nums and return corresponding dates
        case _ if len(choice_nums) > 0:
            return [match_date_by_index(num) for num in choice_nums]

        # check for valid class date strings and return corresponding dates
        case _ if len(choice_dates) > 0:
            return [match_date_by_value(date) for date in choice_dates]

        # no match
        case _:
            raise InvalidSelectionInputError(
                f"input {entry} does not match any of the required formats"
            )

    # match str(entry):
    #     # matches "1", "12", "13", etc.,
    #     case _ if re.fullmatch(r"^\d{1,2}$", entry):
    #         choice: int = int(entry)
    #         # when printing out the available class dates to the user,
    #         # the dates are printed out with each index + 1 to start the count from 1
    #         # hence the last option for all dates is len(dates_list) + 1 and in this case
    #         if choice != len(dates_list) + 1:
    #             return [match_date_by_index(choice)]
    #         else:
    #             # a copy of the actual dates_list is returned.
    #             return dates_list.copy()

    #     # matches "1, 2, 3," ; "12, 1, 2"
    #     case _ if re.fullmatch(r"^(\d{1,2},\s*)+\d{1,2}(?:,|\b)$", entry):
    #         # remove any trailing commas if present
    #         entry = entry.removesuffix(",")

    #         # split `entry` with "," and not ", " which is the value of `COMMA_DELIM`
    #         choices_str: list[str] = entry.split(COMMA_DELIM.strip())

    #         # strip any sequence of characters in `choices_str` with trailing or leading whitespaces
    #         choices_str = [char_seq.strip() for char_seq in choices_str]

    #         # perform match_date_by_index on each string of choices_str after converting to int
    #         return [match_date_by_index(int(num_char)) for num_char in choices_str]

    #     # matches "12/11/2030", "09/03/2004"
    #     case _ if re.fullmatch(r"^\d{2}/\d{2}/\d{4}$", entry):
    #         return [match_date_by_value(entry)]

    #     # matches "12/11/2023, 01/05/1019"; "14/09/2007, 13/02/2014,"
    #     case _ if re.fullmatch(
    #         r"^(\d{2}/\d{2}/\d{4},\s)+\d{2}/\d{2}/\d{4}(?:,|\b)$", entry
    #     ):
    #         # remove any trailing commas if present.
    #         entry = entry.removesuffix(",")

    #         # split `entry` with "," and not ", " which is the value of `COMMA_DELIM`
    #         choices_str = entry.split(COMMA_DELIM.strip())

    #         # strip any sequence of characters in `choices_str` with trailing or leading whitespaces
    #         choices_str = [char_seq.strip() for char_seq in choices_str]

    #         # perform match_date_by_value on each string of choices_str
    #         return [match_date_by_value(choice_str) for choice_str in choices_str]

    #     case _ if re.fullmatch(
    #         r"^\s*((\d+\s*-\s*\d+\s*)|(\d+\s*))((,\s*\d+\s*-\s*\d+\s*)|(,\s*\d+\s*))*(?:,|\b)$",
    #         entry,
    #     ) is not None:
    #         entry = entry.strip()
    #         entries = entry.split(COMMA)
    #         entries = [entry.strip() for entry in entries]
    #         values: list[int] = []
    #         for entry in entries:
    #             match str(entry):
    #                 case _ if re.fullmatch(r"^\s*\d+\s*$", entry) is not None:
    #                     entry = entry.strip()
    #                     entries = entry.split(COMMA)
    #                     entries = [entry.strip() for entry in entries]
    #                     new_values: list[int] = [int(entry) for entry in entries]
    #                     values.extend(new_values)
    #                 case _ if re.fullmatch(r"^\s*(\d+\s*-\s*\d+)$", entry) is not None:
    #                     entry = entry.strip()
    #                     entries = entry.split(HYPHEN)
    #                     entries = [entry.strip() for entry in entries]
    #                     start = int(entries[0])
    #                     end = int(entries[1])
    #                     if start >= end:
    #                         raise InvalidSelectionInputError(
    #                             f"input {entry} does not match any of the required formats because its start is greater than or equal to the end"
    #                         )
    #                     if end == len(dates_list) + 1:
    #                         raise InvalidSelectionInputError(
    #                             f"input {entry} uses the hyphen (-) to mark ranges, hence, it cannot be used with the number indicator that selects all entries."
    #                         )
    #                     values.extend(list(range(start, end + 1)))
    #                 case _:
    #                     raise InvalidSelectionInputError(
    #                         f"input {entry} does not match any of the required formats"
    #                     )
    #         set_of_values: set[int] = set(values)
    #         values = list(set_of_values)
    #         values.sort()
    #         return [match_date_by_index(value) for value in values]

    #     case "all":
    #         return dates_list.copy()

    #     # no match
    #     case _:
    #         raise InvalidSelectionInputError("")
