"""Parse month input to month numbers."""

import re

from ..constants import COMMA, SEMI, SPACE_DELIM
from ..errors import Result


def parse_month(entry: str) -> Result[list[int]]:
    """Parse month input to 1-based month numbers.

    Accepts single or comma/semicolon-separated month names (full or abbreviated),
    month numbers (1-12), or zero-padded month numbers (01-12).

    Args:
        entry (str): Month input string (e.g., "June", "6", "June, July", "6;7").

    Returns:
        Result[list[int]]: Ok with list of month numbers (1-12) or Err with diagnostic message.
    """
    entry = entry.strip()

    delimiter = (
        COMMA
        if COMMA in entry
        else SEMI
        if SEMI in entry
        else SPACE_DELIM
        if SPACE_DELIM in entry
        else None
    )

    if delimiter is not None:
        parts = [p.strip() for p in entry.split(delimiter) if p.strip() != ""]
        months: list[int] = []
        for part in parts:
            result = parse_single_month(part)
            if result.is_err():
                return result.propagate()
            months.append(result.unwrap())
        return Result.ok(sorted(set(months)))

    result = parse_single_month(entry)
    if result.is_err():
        return result.propagate()
    return Result.ok([result.unwrap()])


def parse_single_month(entry: str) -> Result[int]:
    """Parse a single month entry to month number.

    Args:
        entry (str): Single month input string.

    Returns:
        Result[int]: Ok with month number (1-12) or Err with diagnostic message.
    """
    entry = entry.strip().lower()

    match entry:
        case _ if re.fullmatch(r"(january|jan)", entry):
            return Result.ok(1)
        case _ if re.fullmatch(r"(february|feb)", entry):
            return Result.ok(2)
        case _ if re.fullmatch(r"(march|mar)", entry):
            return Result.ok(3)
        case _ if re.fullmatch(r"(april|apr)", entry):
            return Result.ok(4)
        case _ if re.fullmatch(r"may", entry):
            return Result.ok(5)
        case _ if re.fullmatch(r"(june|jun)", entry):
            return Result.ok(6)
        case _ if re.fullmatch(r"(july|jul)", entry):
            return Result.ok(7)
        case _ if re.fullmatch(r"(august|aug)", entry):
            return Result.ok(8)
        case _ if re.fullmatch(r"(september|sep|sept)", entry):
            return Result.ok(9)
        case _ if re.fullmatch(r"(october|oct)", entry):
            return Result.ok(10)
        case _ if re.fullmatch(r"(november|nov)", entry):
            return Result.ok(11)
        case _ if re.fullmatch(r"(december|dec)", entry):
            return Result.ok(12)
        case _ if re.fullmatch(r"\d{1,2}", entry):
            month_num = int(entry)
            if 1 <= month_num <= 12:
                return Result.ok(month_num)
            return Result.err(f"Month number must be between 1 and 12, got {month_num}")
        case _:
            return Result.err(f"Invalid month format: '{entry}'")
