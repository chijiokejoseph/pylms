from ..errors import Result
from .custom_inputs import input_num


def input_option(
    options: list[str], title: str = "Menu", prompt: str = ""
) -> Result[tuple[int, str]]:
    """
    Prompts the user to select an option from a list and returns the selected option's index and value.

    This function displays a list of options to the user with an optional prompt and prompt message. The user is prompted to enter an integer corresponding to their choice. The function validates the input to ensure it is within the range of available options. If the input is valid, it returns the index and the selected option as a tuple. If the input is invalid, it raises an `InvalidInputError` after a specified number of attempts.

    :param options: A list of strings representing the options available for selection.
    :type options: list[str]

    :param prompt: An optional prompt to display above the list of options. Defaults to "Select from the following: ".
    :type prompt: str, optional

    :param prompt: An optional prompt message to display before the input. Defaults to an empty string.
    :type prompt: str, optional

    :return: A result containing a tuple that contains the index of the selected option (1-based) and the selected option itself.
    :rtype: Result[tuple[int, str]]

    """

    menu_bars = "=" * 5

    # Print the prompt above the options list
    print(f"\n{menu_bars} 🗓️ {title} 🗓️ {menu_bars}")

    # Enumerate and print each option with its index starting from 1
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    print(f"{menu_bars} 🗓️ {title} 🗓️ {menu_bars}")

    prompt = f"\n{prompt}\nSelect an Option" if prompt != "" else "\nSelect an Option"
    # Prompt the user to input a number corresponding to their choice
    result = input_num(
        prompt,
        1,
        diagnosis=f"The number you have entered does not match the range 1 - {len(options)}, hence it is invalid",
        test_fn=lambda x: 1 <= x <= len(options),
    )
    if result.is_err():
        return result.propagate()
    choice = result.unwrap()
    # Cast the input to int

    # Calculate zero-based index for list access
    choice_idx: int = choice - 1

    # Return the 1-based choice and the corresponding option string
    return Result.ok((choice, options[choice_idx]))
