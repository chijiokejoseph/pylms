from pylms.cli.option_input import input_option


def interact(menu: list[str]) -> int:
    """
    Displays a menu of options to the user and captures the user's selection.
    Utilizes the `input_option` function to present the menu and retrieve the user's choice.
    
    :param menu: A list of strings representing the menu options to be displayed.
    :type menu: list[str]
    
    :return: The index of the selected option.
    :rtype: int
    """
    
    idx, _ = input_option(menu)
    return idx
