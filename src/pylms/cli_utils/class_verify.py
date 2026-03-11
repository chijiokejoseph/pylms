import re

from ..constants import COMMA, SEMI


def verify_class(entry: str) -> bool:
    """Validate a user's date-selection input string.

    Accepts several input forms commonly used to select class dates:
    - a single 1- or 2-digit index (e.g. "1")
    - a comma-separated list of indices (e.g. "1, 2")
    - a single date in "dd/mm/yyyy" form
    - a comma-separated list of dates in "dd/mm/yyyy" form
    - ranges of indices (e.g. "1-5")
    - the token "all"
    The function returns True when `entry` matches one of the accepted formats.

    Args:
        entry (str): The input string to validate.

    Returns:
        bool: True if `entry` matches an accepted date-selection format,
            False otherwise.
    """
    entry = entry.strip().lower()

    if entry == "all":
        return True

    # Single or double digit number
    if re.fullmatch(r"\d{1,2}", entry):
        return True

    # Date format dd/mm/yyyy
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", entry):
        return True

    # Comma-separated list
    delim = COMMA if COMMA in entry else SEMI if SEMI in entry else None
    if delim is not None:
        parts = [p.strip() for p in entry.split(delim) if p.strip() != ""]
        for part in parts:
            # Each part should be a number, range, or date
            if not (
                re.fullmatch(r"\d{1,2}", part)
                or re.fullmatch(r"\d+-\d+", part)
                or re.fullmatch(r"\d{2}/\d{2}/\d{4}", part)
            ):
                return False
        return True

    # Range format
    if re.fullmatch(r"\d+\s*-\s*\d+", entry):
        return True

    return False
