from pylms.cli.option_input import input_option
from pylms.cli.utils import parse_response


def interact(menu: list[str], trials: int = 5) -> int:
    """
    the main dialog function between the program and the user. this function prints out a main menu to the user and receives the user's choice.

    Based on a list of defined options, the choice entered by the user is expected to be a number matching the option number for the option the user intends to select.

    This input is then parsed using the private helper functions `_parse` and if the choice entered by the user is not validated, the function repeats the prompt a certain number of times as defined by the argument to `trials`.

    If the user fails to enter a valid input after these repetitive prompts, the function forcefully exits the program.

    :param menu: (list[str]) - A list of options that make up the main menu of the program.
    :type menu: list[str]
    :param trials: (int, optional): the number of times the program will repeatedly prompt the user if the user enters an invalid input. Default to 5.
    :type trials: int, optional

    :returns: option number selected by the user
    :rtype: int
    """

    for _ in range(trials):
        _, choice = input_option(menu)
        parsed_choice: int | None = parse_response(menu, choice)
        if parsed_choice is not None:
            return parsed_choice

    exit(1)
