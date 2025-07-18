"""
The cli package is a package designed to abstract a lot of code used for prompting and parsing responses from a user in the command line on which this program runs. The package includes useful functions such as:

Functions:
interact:  a function that handles the display of the main menu and parsing of all the user's response to the main menu.

input_num: a function that prompts the user to enter a number and implements some internal parsing logic to ensure that only a valid number is returned. It also requires some form of extra validation function to be passed as an argument to ensure that the entered number is not only a valid number but also within a valid range for whatever use case that it is intended for.

input_str: a function that prompts the user to enter a str. Like input_num it requires some form of str validation function to be passed as an argument to validate the entered response.

input_date_str: a function that prompts the user to enter a valid class date as a str. Unlike the input_num and input_str functions, this function does all the validation and parsing internally. Moreover, the dates stored in the program in the path `data/json/dates.json` are used to verify any input entered by the user. This function is primarily used when the user's input must be parsable to one of the class dates stored in the program, if not, the `input_str` function is the preferred choice for input.

input_cleaning_req: a function that prompts the user to confirm that the requirements needed for the initial preprocessing of new registration data for a new cohort are met.

input_email: a function that prompts the user to enter a valid gmail address as a str. Unlike the `input_num` and `input_str` functions, this function does all the validation and parsing internally.
"""

from pylms.cli.custom_inputs import (
    input_num,
    input_str,
)
from pylms.cli.email_input import input_email
from pylms.cli.interact import interact
from pylms.cli.onboard_req import confirm_onboard_req
from pylms.cli.option_input import input_option
from pylms.cli.path_input import input_path, test_path_in
from pylms.cli.record_input import input_record
from pylms.cli.select_class_date import select_class_date
from pylms.cli.select_student import select_student

__all__: list[str] = [
    "interact",
    "input_num",
    "input_record",
    "input_option",
    "input_path",
    "test_path_in",
    "input_str",
    "confirm_onboard_req",
    "input_email",
    "select_class_date",
    "select_student",
]
