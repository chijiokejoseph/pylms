from pylms.cli.custom_inputs import input_str
from pylms.cli.utils import parse_to_dates, val_date_str
from pylms.utils.date.retrieve_dates import retrieve_dates


def select_class_date(msg: str) -> list[str]:
    """
    prompts the user with the argument to `msg` to select a class date from the list of class dates stored in the program and gives the user options for selecting these dates. There are several possible means of selecting a class date:

    If the following is printed to the user:
        1. 13/01/2025
        2. 14/01/2025
        3. 15/01/2025
        4. 16/01/2025
        5. 17/01/2025
        6. all

    then the instructions are:
        - Entering a single option number for a single target class date e.g., **1** -> `13/01/2025`
        - Entering a comma separated entry of integers to target multiple class dates e.g., **1, 2, 3, 5** -> `13/10/2025, 14/01/2025, 15/01/2025, 17/01/2025`
        - Entering a single class date e.g., **13/01/2025** -> `13/01/2025`
        - Entering a comma separated entry of class dates to target multiple class dates e.g., **13/01/2025, 16/01/2025** -> `13/01/2025, 16/01/2025`
        - Entering the option number that matches "all" e.g., **6** -> `13/01/2025, 14/01/2025, 15/01/2025, 16/01/2025, 17/01/2025`
        - Entering a string that matches "all" e.g., **all** -> `13/01/2025, 14/01/2025, 15/01/2025, 16/01/2025, 17/01/2025`

    Based on the user's input, the user's response is parsed and the targeted dates are returned as a `list[str]`. If the user specifies an invalid input, the program forcefully exits.

    :param msg: (str): The prompt message to be displayed to the user before printing out the instructions on how to select the class dates. This message usually states the kind of data for which those class dates are needed.
    :type msg: str

    :returns: a list of selected class dates
    :rtype: list[str]
    """
    # get class dates
    dates_list: list[str] = retrieve_dates()
    dates_list.append(
        "all"
    )  # add all to add an option for selecting all the class_dates at once
    print(msg)
    guide: str = f"""
You can enter the dates using one of the following formats:
    i. Enter the corresponding class number without the `Class` term just the number
    to pick a single date e.g., "Enter date: 1"
    
    ii. Enter the exact class date (which has been printed out in the form dd/mm/yyyy)
    to pick that single date
    
    iii. Enter comma separated values of the class numbers without the `Class` term.
    e.g., "Enter date: 1, 2, 3"
    
    iv. Enter comma separated values of the exact dates for which forms should be generated
    e.g., "Enter date: 13/01/2025, 14/01/2025"
    PS: This should match the dates on the menu displayed above
    else the program will fail.
    
    v. {len(dates_list)} if all the available dates are being targeted.
    It must be entered as a single number i.e., "1, 2, {len(dates_list)}" is invalid.
    e.g., "Enter date: 16"
    
    v. "all" if all the available dates are being targeted.
    It must be entered solely by itself i.e., "13/01/2025, all" is invalid.
    e.g., "Enter date: all"
    """
    # prints out the instructions on how to select class dates
    print(guide)

    print("The class dates with their class numbers are printed below")
    # print out each class date and an option number for each class date
    for i, each_date in enumerate(dates_list, start=1):
        print(f"Class {i}. {each_date}")

    # uses `input_str` and the validation function `_date_val_input` to validate user input
    response: str = input_str(
        "Enter the relevant date(s): ",
        val_date_str,
        diagnosis="Your input is invalid. Please confirm that your response matches any of the constraints stated above.",
    )
    # parses the user input with the function _parse_date
    class_dates: list[str] = parse_to_dates(response)
    print(f"You have selected {class_dates}\n")
    return class_dates
