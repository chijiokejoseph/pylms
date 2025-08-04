import pandas as pd
from pylms.cli import input_str, input_option, input_path
from pylms.utils import read_data, DataStream
from pylms.constants import SEMI, COMMA



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


def provide_emails() -> list[str]:
    # List of options for providing email addresses
    provide_emails_formats = [
        "Provide emails as .txt file (one email per line)",
        "Provide emails as .csv file (one email per line)",
        "Provide emails as .xlsx file (single col with emails)",
        "Provide emails as input delimited by either ';' or ','",
    ]

    # Prompt user to select the format of the email input
    pos, format_msg = input_option(
        provide_emails_formats, prompt="Select the format to provide the email in"
    )

    # Get the file path or input string based on the selected format
    filepath = input_path(f"{format_msg}: ")

    # Read emails based on the selected input format
    match pos:
        case 1 | 2:
            # Read emails from a text or CSV file, one email per line
            with filepath.open() as file:
                emails: list[str] = file.readlines()
                emails = [email.strip() for email in emails]
        case 3:
            # Read emails from an Excel file with a single column
            data: pd.DataFrame = read_data(filepath)
            stream: DataStream[pd.DataFrame] = DataStream[pd.DataFrame](
                data, verify_excel
            )
            emails = stream.as_ref().iloc[:, 0].tolist()
        case _:
            # Read emails from a delimited input string
            response: str = input_str(f"{format_msg}: ")
            emails = (
                response.split(SEMI)
                if SEMI in response
                else response.split(",")
                if COMMA in response
                else [response]
            )
            emails = [email.strip() for email in emails if email.strip() != ""]
    return emails
