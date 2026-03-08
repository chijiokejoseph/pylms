"""Interactive email input selection."""

from ..errors import Result
from .custom_inputs import input_str
from .emails_file import read_emails_csv, read_emails_file
from .emails_string import read_emails_string
from .emails_txt import read_emails_txt
from .option_input import input_option
from .path_input import input_path


def input_emails() -> Result[list[str]]:
    """Interactive function to select email input method and collect emails.

    Provides user with options to:
    1. Provide emails from .txt file
    2. Provide emails from .csv file
    3. Provide emails from .xlsx file
    4. Provide emails as delimited string

    Returns:
        Result[list[str]]: List of valid emails or error.
    """
    # Define input method options
    options = [
        "Provide emails as .txt file (one email per line)",
        "Provide emails as .csv file (first string column)",
        "Provide emails as .xlsx file (first string column)",
        "Provide emails as input delimited by ';' or ','",
    ]

    # Display menu and get user selection
    result = input_option(options, prompt="Select the format to provide emails")
    if result.is_err():
        return result.propagate()

    idx, format_msg = result.unwrap()

    # Handle file-based inputs
    if idx in [1, 2, 3]:
        path_result = input_path(f"{format_msg}: ")
        if path_result.is_err():
            return path_result.propagate()
        filepath = path_result.unwrap()

        # Delegate to appropriate file reader
        match idx:
            case 1:
                return read_emails_txt(filepath)
            case 2:
                return read_emails_csv(filepath)
            case 3:
                return read_emails_file(filepath)
            case _:
                raise ValueError("unreachable")

    # Handle string input
    result = input_str(f"{format_msg}: ")
    if result.is_err():
        return result.propagate()

    raw_input = result.unwrap()
    return read_emails_string(raw_input)
