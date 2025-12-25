from pathlib import Path

import pandas as pd

from ..cli_utils import verify_email
from ..constants import COMMA, SEMI
from ..data.data_read import read
from ..data.datastream import DataStream
from ..errors import Result, eprint
from .custom_inputs import input_str
from .option_input import input_option
from .path_input import input_path


def verify_excel(data: pd.DataFrame) -> bool:
    """Validate that an Excel-read DataFrame is a single non-empty column.

    This function checks that the provided DataFrame is not empty and that it
    contains exactly one column. It is typically used to validate Excel files
    that are expected to contain a single column of values (for example, a
    single-column list of email addresses).

    Args:
        data (pd.DataFrame): The DataFrame to validate.

    Returns:
        bool: True if the DataFrame is non-empty and has exactly one column,
            False otherwise.
    """
    # Check if the data is empty
    if data.empty:
        # If the data is empty, it's not valid
        return False

    # Check if the data has more than one column
    elif len(data.columns.tolist()) > 1:
        # If the data has more than one column, it's not valid
        return False

    # If the data passes both checks, it's valid
    else:
        return True


def provide_emails() -> Result[list[str]]:
    # List of options for providing email addresses
    provide_emails_formats = [
        "Provide emails as .txt file (one email per line)",
        "Provide emails as .csv file (one email per line)",
        "Provide emails as .xlsx file (single col with emails)",
        "Provide emails as input delimited by either ';' or ','",
    ]

    # Prompt user to select the format of the email input
    result = input_option(
        provide_emails_formats, prompt="Select the format to provide the email in"
    )
    if result.is_err():
        return result.propagate()
    pos, format_msg = result.unwrap()

    # Read emails based on the selected input format
    match pos:
        case 1 | 2 | 3:
            # Get the file path or input string based on the selected format
            path_result: Result[Path] = input_path(f"{format_msg}: ")
            if path_result.is_err():
                return path_result.propagate()
            filepath: Path = path_result.unwrap()

            match pos:
                case 1 | 2:
                    # Read emails from a text or CSV file, one email per line
                    if not filepath.suffix.endswith(
                        "txt"
                    ) and not filepath.suffix.endswith("csv"):
                        msg: str = f"Error: Invalid file type. {filepath} is not a txt or csv file. Please select a .txt or .csv file."
                        eprint(msg)
                        return Result.err(msg)
                    with filepath.open() as file:
                        emails: list[str] = file.readlines()
                        emails = [email.strip() for email in emails]
                case _:
                    # Read emails from an Excel file with a single column
                    data = read(filepath)
                    if data.is_err():
                        return data.propagate()
                    data = data.unwrap()

                    stream = DataStream.new(data, verify_excel)
                    if stream.is_err():
                        return stream.propagate()
                    stream = stream.unwrap()

                    emails = stream.as_ref().iloc[:, 0].tolist()
        case _:
            result = input_str(f"{format_msg}: ")
            if result.is_err():
                return result.propagate()

            # Read emails from a delimited input string
            response: str = result.unwrap()
            emails = (
                response.split(SEMI)
                if SEMI in response
                else response.split(COMMA)
                if COMMA in response
                else [response]
            )
            emails = [email.strip() for email in emails if email.strip() != ""]

    emails = [email for email in emails if verify_email(email)]

    if len(emails) == 0:
        msg = "Error: No valid emails found in the file."
        eprint(msg)
        return Result.err(msg)

    return Result.ok(emails)
