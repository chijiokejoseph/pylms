from ..errors import Result
from .custom_inputs import input_num


def input_option(
    options: list[str], title: str = "Menu", prompt: str = ""
) -> Result[tuple[int, str]]:
    """Prompt the user to select an option from a list and return the selection.

    Displays a numbered menu of `options` with an optional `title` and
    `prompt`. Prompts the user to enter a number corresponding to their
    choice, validates that the input falls within the available range, and
    returns a tuple containing the 1-based index and the selected option
    string inside a `Result.ok`. If the interactive prompt fails, the error
    `Result` is propagated.

    Args:
        options (list[str]): List of option strings to display.
        title (str): Title displayed above the menu. Defaults to "Menu".
        prompt (str): Optional prompt text shown above the input prompt.

    Returns:
        Result[tuple[int, str]]: Ok result with a tuple of (1-based index,
            option string), or an error `Result` propagated from the input
            helper.
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


def input_bool(prompt: str) -> Result[bool]:
    menu = ["Yes", "No"]
    result = input_option(menu, "Confirm Menu", prompt)
    if result.is_err():
        return result.propagate()

    idx, _ = result.unwrap()

    return Result.ok(idx == 1)
