from ..errors import Result
from .option_input import input_option


def interact(menu: list[str]) -> Result[int]:
    """
    Displays a menu of options to the user and captures the user's selection.
    Utilizes the `input_option` function to present the menu and retrieve the user's choice.

    :param menu: A list of strings representing the menu options to be displayed.
    :type menu: list[str]

    :return: The index of the selected option.
    :rtype: int
    """

    result = input_option(menu)
    if result.is_err():
        return result.propagate()
    idx, _ = result.unwrap()
    return Result[int].ok(idx)
