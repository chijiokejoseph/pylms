import re
from datetime import datetime

from ..constants import (
    COMMA_DELIM,
    DATE_FMT,
    NA,
    SPACE_DELIM,
)


def fmt_phone(entry: str) -> str:
    """Format phone number entry for display.
    
    Processes phone number strings to remove country codes and handle multiple numbers.
    
    Args:
        entry (str): Raw phone number string.
        
    Returns:
        str: Formatted phone number or empty string if invalid.
    """
    entry = entry.strip()
    match str(entry):
        case _ if entry.startswith(NA):
            return ""
        case _ if re.fullmatch(r"^\s*\d+\s*", entry) is not None:
            entry = entry.strip()
            return entry[1:]
        case _ if re.fullmatch(r"^\s*\d+\s+\d+\s*$", entry) is not None:
            entries = entry.split(SPACE_DELIM)
            entries = [entry[1:] for entry in entries]
            return COMMA_DELIM.join(entries)
        case _:
            return ""


def fmt_date(date_str: str) -> str:
    """Format date string to ordinal format.
    
    Converts date from DD/MM/YYYY format to "1st January 2024" format.
    
    Args:
        date_str (str): Date string in DD/MM/YYYY format.
        
    Returns:
        str: Formatted date with ordinal day and full month name.
    """
    date_form = datetime.strptime(date_str, DATE_FMT)
    day = date_form.day
    month = date_form.strftime("%B")
    year = date_form.year
    day_str = str(day)
    last_digit = int(day_str[-1])
    ordinal_map = {
        1: "st",
        2: "nd",
        3: "rd",
    }
    default = "th"
    ordinal = ordinal_map.get(last_digit, default)
    day_str += ordinal
    return f"{day_str} {month} {year}"
