from pylms.cli.custom_inputs import input_str
from pylms.cli.utils import parse_to_dates, val_date_str
from pylms.errors import Result
from pylms.utils.date.retrieve_dates import retrieve_dates


def select_class_date(
    msg: str, src_dates_list: list[str] | None = None
) -> Result[list[str]]:
    """
    Prompts the user to select a class date from the list of class dates.

    The user can enter dates in the following formats:

    - Single class number (e.g. "1")
    - Exact date (e.g. "13/01/2025")
    - Comma-separated class numbers (e.g. "1, 2, 3")
    - Comma-separated exact dates (e.g. "13/01/2025, 14/01/2025")
    - Date ranges (e.g. "1 - 3", "1 -3, 5, 7 - 10")
    - "all" to select all available dates

    The function prints out the instructions on how to select class dates and the class dates with their class numbers,
    and then uses `input_str` to receive user input before validating it.
    Finally, it parses the user input and returns the selected class date(s) as a list of str.

    :param msg: (str) - The message to display before prompting the user for input.
    :type msg: str

    :param src_dates_list: (list[str] | None) - An optional list of class dates to choose from. If not provided, it defaults to retrieving dates from the system.
    :type src_dates_list: list[str] | None


    :return: A result containing the list of class dates selected by the user.
    :rtype: Result[list[str]]
    """

    # get class dates
    all_dates: list[str] = retrieve_dates()
    dates_list: list[str] = src_dates_list if src_dates_list is not None else all_dates
    if src_dates_list is None:
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
    print(guide)

    print("The class dates with their class numbers are printed below")
    # print out each class date and an option number for each class date
    for each_date in dates_list:
        i: int = (
            all_dates.index(each_date) + 1 if each_date != "all" else len(all_dates) + 1
        )
        print(f"Class {i}. {each_date}")

    # uses `input_str` and the validation function `_date_val_input` to validate user input
    result: Result[str] = input_str(
        "Enter the relevant date(s): ",
        val_date_str,
        diagnosis="Your input is invalid. Please confirm that your response matches any of the constraints stated above.",
    )
    if result.is_err():
        return Result[list[str]].err(result.unwrap_err())
    response: str = result.unwrap()
    # parses the user input with the function _parse_date
    class_dates: list[str] = parse_to_dates(response)
    print(f"You have selected {class_dates}\n")
    return Result[list[str]].ok(class_dates)
