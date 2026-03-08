"""Read emails from text file."""

from pathlib import Path

from ..cli_utils import verify_email, verify_gmail
from ..errors import Result, eprint


def read_emails_txt(filepath: Path, gmail: bool = True) -> Result[list[str]]:
    """Read and validate emails from a text file (one email per line).

    Args:
        filepath: Path to text file containing emails.
        gmail: True to use Gmail email validation, False otherwise.

    Returns:
        Result[list[str]]: List of valid emails or error.
    """
    if not filepath.suffix.endswith("txt"):
        msg = f"Error: Invalid file type. {filepath} is not a txt file."
        eprint(msg)
        return Result.err(msg)

    with filepath.open() as file:
        emails = file.readlines()
        emails = [email.strip() for email in emails]

    validator = verify_gmail if gmail else verify_email

    # Filter valid emails
    emails = [email for email in emails if validator(email)]

    if len(emails) == 0:
        msg = "Error: No valid emails found in the file."
        eprint(msg)
        return Result.err(msg)

    return Result.ok(emails)
