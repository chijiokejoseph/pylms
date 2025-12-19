from pathlib import Path

import pandas as pd

from ..cli_utils import validate_email
from ..constants import COMMA, SEMI
from ..data.data_read import read
from ..data.datastream import DataStream
from ..errors import Result, eprint
from .custom_inputs import input_str
from .option_input import input_option
from .path_input import input_path


def verify_excel(data: pd.DataFrame) -> bool:
    """
    Verify that the provided Excel data is valid.

    :param data: (pd.DataFrame) - The Excel data to verify.
    :type data: pd.DataFrame

    :return: (bool) - True if the data is valid, False otherwise.
    :rtype: bool
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
    option_result: Result[tuple[int, str]] = input_option(
        provide_emails_formats, prompt="Select the format to provide the email in"
    )
    if option_result.is_err():
        return option_result.propagate()
    pos, format_msg = option_result.unwrap()

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
                        return Result.err(ValueError(msg))
                    with filepath.open() as file:
                        emails: list[str] = file.readlines()
                        emails = [email.strip() for email in emails]
                case _:
                    # Read emails from an Excel file with a single column
                    data = read(filepath)
                    if data.is_err():
                        return data.propagate()
                    data = data.unwrap()
                    stream: DataStream[pd.DataFrame] = DataStream(data, verify_excel)
                    emails = stream.as_ref().iloc[:, 0].tolist()
        case _:
            email_result: Result[str] = input_str(f"{format_msg}: ")
            if not email_result.is_ok():
                return Result.err(ValueError("Invalid emails passed in"))
            # Read emails from a delimited input string
            response: str = email_result.unwrap()
            emails = (
                response.split(SEMI)
                if SEMI in response
                else response.split(COMMA)
                if COMMA in response
                else [response]
            )
            emails = [email.strip() for email in emails if email.strip() != ""]
    emails = [email for email in emails if validate_email(email)]
    if len(emails) == 0:
        msg = "Error: No valid emails found in the file."
        eprint(msg)
        return Result.err(ValueError(msg))
    return Result.ok(emails)
