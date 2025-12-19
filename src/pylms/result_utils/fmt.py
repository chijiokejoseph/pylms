import re
from datetime import datetime

from ..constants import (
    COMMA_DELIM,
    DATE_FMT,
    NA,
    SPACE_DELIM,
)


def fmt_phone(entry: str) -> str:
    entry = entry.strip()
    match str(entry):
        case _ if entry.startswith(NA):
            return ""
        case _ if re.fullmatch(r"^\s*\d+\s*", entry) is not None:
            entry = entry.strip()
            return entry[1:]
        case _ if re.fullmatch(r"^\s*\d+\s+\d+\s*$", entry) is not None:
            entries: list[str] = entry.split(SPACE_DELIM)
            entries = [entry[1:] for entry in entries]
            return COMMA_DELIM.join(entries)
        case _:
            return ""


def fmt_date(date_str: str) -> str:
    date_form: datetime = datetime.strptime(date_str, DATE_FMT)
    day: int = date_form.day
    month: str = date_form.strftime("%B")
    year: int = date_form.year
    day_str: str = str(day)
    last_digit: int = int(day_str[-1])
    ordinal_map: dict[int, str] = {
        1: "st",
        2: "nd",
        3: "rd",
    }
    default: str = "th"
    ordinal: str = ordinal_map.get(last_digit, default)
    day_str += ordinal
    return f"{day_str} {month} {year}"
