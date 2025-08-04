def parse_response(menu: list[str], response: str) -> int | None:
    """
    Parse the user's response from a menu selection.
    This function validates the user's input against the provided menu options
    and returns the selected option as an integer if valid, otherwise returns None.

    :param menu: (list[str]) - The list of menu options.
    :type menu: list[str]

    :param response: (str) - The user's response to the menu selection.
    :type response: str

    :return: (int | None) - The selected option as an integer if valid, otherwise None.
    :rtype: int | None
    """
    # Normalize the response string to lowercase and strip whitespace
    response = response.lower().strip()

    try:
        # Attempt to convert the response to an integer selection
        selection: int = int(response)
    except ValueError:
        # Handle the case where conversion to integer fails
        print("Invalid option received from the user, please enter a valid number.\n")
        return None

    # Check if the selection is within the valid range of menu options
    if selection > len(menu) or selection <= 0:
        print(f"Invalid choice selected only inputs from 1 - {len(menu)} are valid.")
        return None

    # Confirm the selected option to the user
    print(f"You have selected option {selection}: {menu[selection - 1]}\n")
    return selection

