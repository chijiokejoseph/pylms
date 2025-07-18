def parse_response(menu: list[str], response: str) -> int | None:
    """
    parses the `response` argument. Its operation can be broken into two (2) stages:

    1. convert `response` to int:

        - If `response` is convertible to int continue with int value.

        - If `response` is not convertible to int continue with None after printing a warning message

        The parsed value from this stage is stored in var `selection`

    2. match `selection` (int or None):

        - if `selection` is None, return None
        - if `selection` is int, but `selection` > len(`menu`) or `selection` < 1 i.e., **selection - 1** does not correspond to a valid index of `menu` print a warning message concerning this then return None
        - else print the option corresponding to `selection` and return the value of `selection`


    :param menu: (list[str]) - A list of strings which contains the strings displayed to the user as part of the main menu of the program
    :type menu: list[str]
    :param response: (str) - The response entered by the user
    :type response: str

    :return: An int if parsing is successful else None:
    :rtype: int | None
    """

    response = response.lower().strip()

    try:
        selection: int = int(response)
    except ValueError:
        print("Invalid option received from the user, please enter a valid number.\n")
        return None

    if selection > len(menu) or selection < 1:
        print(f"Invalid choice selected only inputs from 1 - {len(menu)} are valid.")
        return None

    print(f"You have selected option {selection}: {menu[selection - 1]}\n")
    return selection
