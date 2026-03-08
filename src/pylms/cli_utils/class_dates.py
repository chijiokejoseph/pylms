import re

from ..constants import COMMA


def parse_class_dates(entry: str) -> list[str]:
    """Parse a date string or comma-separated date strings into a list.

    Accepts a single date string in the form 'dd/mm/yyyy' or a comma-separated
    list of such date strings and returns a list of cleaned date strings.
    Leading or trailing commas are tolerated and whitespace around entries is
    trimmed.

    Args:
        entry (str): A date string or comma-separated date strings in the
            format 'dd/mm/yyyy'.

    Returns:
        list[str]: Parsed date strings. Returns an empty list when the input
            does not match the supported formats.
    """
    entry = entry.strip()
    
    # Single date
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", entry):
        return [entry]
    
    # Comma-separated dates
    if COMMA in entry:
        entry = entry.rstrip(",")
        parts = [p.strip() for p in entry.split(",") if p.strip() != ""]
        # Validate all parts are dates
        if all(re.fullmatch(r"\d{2}/\d{2}/\d{4}", p) for p in parts):
            return parts
    
    return []
