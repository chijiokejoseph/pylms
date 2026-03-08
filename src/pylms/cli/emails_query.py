"""General query function for email input."""

from pathlib import Path

from ..cli_utils import verify_name
from ..errors import ForcedExitError, Result
from ..info import print_info
from .custom_inputs import input_str
from .emails_file import read_emails_file
from .emails_inputs import input_emails
from .emails_mode import EmailInputMode
from .emails_parse import query_emails_parse
from .emails_string import read_emails_string
from .emails_txt import read_emails_txt


def query_emails() -> Result[list[str]]:
    """General interactive function to collect email addresses.

    Prompts user for a query string that can be:
    - Path to .txt file
    - Path to .csv file
    - Path to .xlsx/.xls file
    - Comma/semicolon delimited string of emails

    Parses the query and applies appropriate input method. Falls back to
    interactive selection if parsing fails. Loops until valid input or ForcedExitError.

    Returns:
        Result[list[str]]: List of valid emails or ForcedExitError.
    """
    # Define prompt message
    prompt = """Enter email input:
  - Path to .txt file (one email per line)
  - Path to .csv file (one email per line)
  - Path to .xlsx file (first string column)
  - Comma/semicolon delimited emails
Query: """

    # Loop until valid input or forced exit
    while True:
        # Prompt for query input
        result = input_str(prompt, verify_name, diagnosis="Query cannot be empty")

        # Check for forced exit
        if result.is_err() and isinstance(result.error, ForcedExitError):
            return result.propagate()
        elif result.is_err():
            result.print_if_err()
            continue

        # Parse query string
        query = result.unwrap()
        parse_result = query_emails_parse(query)

        # Check parse result - if parsing fails, fall back to interactive input
        if parse_result.is_err() and isinstance(parse_result.error, ForcedExitError):
            return parse_result.propagate()
        elif parse_result.is_err():
            parse_result.print_if_err()
            print_info("Falling back to interactive input...\n")
            return input_emails()

        # Apply appropriate input method
        input_type, value = parse_result.unwrap()

        if isinstance(value, Path):
            match input_type:
                case EmailInputMode.TXT:
                    emails_result = read_emails_txt(value)
                case _:
                    emails_result = read_emails_file(value)
        else:
            emails_result = read_emails_string(value)

        # Check result
        if emails_result.is_err() and isinstance(emails_result.error, ForcedExitError):
            return emails_result.propagate()
        elif emails_result.is_err():
            emails_result.print_if_err()
            continue

        # Return successful result
        return emails_result
