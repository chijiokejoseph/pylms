from ..errors import Result
from .option_input import input_option


def interact(menu: list[str]) -> Result[int]:
    """Prompt the user with a menu and return the selected option index.

    Displays the provided list of `menu` options using `input_option`, validates
    the user's selection, and returns the selected 1-based index wrapped in a
    `Result`. Any error `Result` produced by the input helper is propagated.

    Args:
        menu (list[str]): List of option strings to present to the user.

    Returns:
        Result[int]: Ok containing the selected 1-based index, or an Err
            propagated from the input helper.
    """

    result = input_option(menu)
    if result.is_err():
        return result.propagate()

    idx, _ = result.unwrap()
    return Result.ok(idx)
