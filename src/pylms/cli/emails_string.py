"""Parse emails from raw string input."""

from ..cli_utils import verify_email, verify_gmail
from ..constants import COMMA, SEMI
from ..errors import Result, eprint


def read_emails_string(raw_input: str, gmail: bool = True) -> Result[list[str]]:
    """Parse and validate emails from a delimited string.

    Splits input by semicolons or commas and validates each email.

    Args:
        raw_input: String containing emails delimited by ';' or ','.

    Returns:
        Result[list[str]]: List of valid emails or error.
    """
    # Split by semicolon or comma
    emails = (
        raw_input.split(SEMI)
        if SEMI in raw_input
        else raw_input.split(COMMA)
        if COMMA in raw_input
        else [raw_input]
    )

    # Strip whitespace
    emails = [email.strip() for email in emails if email.strip() != ""]

    validator = verify_gmail if gmail else verify_email

    # Filter valid emails
    emails = [email for email in emails if validator(email)]

    if len(emails) == 0:
        msg = "Error: No valid emails found in input."
        eprint(msg)
        return Result.err(msg)

    return Result.ok(emails)
