"""Read emails from CSV or Excel file."""

from pathlib import Path

import polars.selectors as cs

from ..cli_utils import verify_email, verify_gmail
from ..data import read
from ..errors import Result, eprint


def read_emails_csv(filepath: Path) -> Result[list[str]]:
    """Read and validate emails from a CSV file (one email per line).

    Args:
        filepath: Path to CSV file containing emails.

    Returns:
        Result[list[str]]: List of valid emails or error.
    """
    if not filepath.suffix.endswith("csv"):
        msg = f"Error: Invalid file type. {filepath} is not a csv file."
        eprint(msg)
        return Result.err(msg)

    with filepath.open() as file:
        emails = file.readlines()
        emails = [email.strip() for email in emails]

    # Filter valid emails
    emails = [email for email in emails if verify_email(email)]

    if len(emails) == 0:
        msg = "Error: No valid emails found in the file."
        eprint(msg)
        return Result.err(msg)

    return Result.ok(emails)


def read_emails_file(filepath: Path, gmail: bool = True) -> Result[list[str]]:
    """Read and validate emails from an Excel file (first string column).

    Args:
        filepath: Path to Excel file containing emails.
        gmail: If True, validates Gmail addresses only. If False, validates any email format.

    Returns:
        Result[list[str]]: List of valid emails or error.
    """
    if not filepath.suffix.endswith(("xlsx", "xls", "csv")):
        msg = f"Error: Invalid file type. {filepath} is not an Excel/CSV file."
        eprint(msg)
        return Result.err(msg)

    # Read Excel file
    data = read(filepath)
    if data.is_err():
        return data.propagate()

    df = data.unwrap()

    # Select first string column
    string_cols = df.select(cs.string())
    if string_cols.width == 0:
        msg = "Error: No string columns found in Excel file."
        eprint(msg)
        return Result.err(msg)

    # Get emails from first string column
    emails = string_cols.to_series().to_list()

    validator = verify_gmail if gmail else verify_email
    # Filter valid emails
    emails = [email for email in emails if isinstance(email, str) and validator(email)]

    if len(emails) == 0:
        msg = "Error: No valid emails found in the file."
        eprint(msg)
        return Result.err(msg)

    return Result.ok(emails)
