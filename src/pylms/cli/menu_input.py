"""Input function for date selection."""

from ..cli_utils import verify_nums
from ..errors import Result
from ..info import print_info
from .custom_inputs import input_str
from .dates_print import print_date_menu


def input_menu(values: list[str], prompt: str = "Select value: ") -> Result[str]:
    """Display date menu and prompt for date input with validation.

    Args:
        dates (list[str]): List of dates to display.
        prompt (str): Prompt message to display.

    Returns:
        Result[str]: Success with user input or error.
    """
    if len(values) == 0:
        return Result.err("No dates available")

    display = values.copy()
    display.append("all")

    print_info(prompt)

    guide = f"""You can enter the serials in the following formats:
    - Single class number (e.g. "1")
    - Comma-separated class numbers (e.g. "1, 2, 3")
    - Date ranges (e.g. "1-3", "1-3, 5, 7-10")
    - "{len(display)}" or "all" to select all available dates
Note: Dates must match the menu displayed below.
    """
    print_info(guide)

    print_date_menu(display)

    result = input_str(
        "Enter the relevant date(s): ",
        verify_nums,
        diagnosis="Your input is invalid. Please confirm that your response matches any of the constraints stated above.",
    )
    return result
