from ..errors import eprint
from ..info import printpass


def parse_response(menu: list[str], response: str) -> int | None:
    """Parse and validate a menu selection response.

    Validate the provided `response` string against the available `menu`
    options. The function attempts to parse `response` as an integer and
    ensures it is within the valid 1-based range of `menu`. When valid the
    selected index (1-based) is returned; otherwise the function returns
    `None`.

    Args:
        menu (list[str]): The list of menu options presented to the user.
        response (str): The user's raw response string.

    Returns:
        int | None: The selected 1-based index when the input is valid, or
            `None` when the input is invalid.
    """
    # Normalize the response string to lowercase and strip whitespace
    response = response.lower().strip()

    try:
        # Attempt to convert the response to an integer selection
        selection: int = int(response)
    except ValueError:
        # Handle the case where conversion to integer fails
        eprint("Invalid option received from the user, please enter a valid number.\n")
        return None

    # Check if the selection is within the valid range of menu options
    if selection > len(menu) or selection <= 0:
        eprint(f"Invalid choice selected only inputs from 1 - {len(menu)} are valid.")
        return None

    # Confirm the selected option to the user
    printpass(f"You have selected option {selection}: {menu[selection - 1]}\n")
    return selection
