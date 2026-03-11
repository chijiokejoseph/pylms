"""Parse and verify number inputs."""

import re

from ..constants import COMMA, HYPHEN, SEMI
from ..errors import Result


def verify_nums(entry: str) -> bool:
    """Verify if entry is valid number input format.
    
    Accepts single numbers, comma/semicolon-separated lists, ranges,
    or combinations of these formats.
    
    Args:
        entry (str): Input string to verify.
        
    Returns:
        bool: True if valid format, False otherwise.
    """
    entry = entry.strip()
    
    # Single number
    if re.fullmatch(r"\d+", entry):
        return True
    
    # Check for valid delimiters and ranges
    if not re.fullmatch(r"[\d\s,;-]+", entry):
        return False
    
    # Split by comma or semicolon
    delimiter = COMMA if COMMA in entry else SEMI if SEMI in entry else None
    if delimiter is None:
        return False
    
    parts = [p.strip() for p in entry.split(delimiter) if p.strip()]
    
    for part in parts:
        # Check if part is single number or range
        if not re.fullmatch(r"\d+", part) and not re.fullmatch(r"\d+\s*-\s*\d+", part):
            return False
    
    return True


def parse_nums(entry: str) -> Result[list[int]]:
    """Parse a string into a list of integers (supports ranges and lists).

    Accepts single numbers, comma/semicolon-separated lists, ranges (for example
    "1-5"), or combinations of these formats. Parsing returns a Result
    containing the parsed integers when successful. When input contains
    invalid formatting a `Result.err` with a diagnostic message is returned.

    Args:
        entry (str): Input string representing one or more integer selections.

    Returns:
        Result[list[int]]: Ok with the parsed list of integers, or Err with a
            diagnostic message when parsing fails.
    """
    entry = entry.strip()
    
    # Single number
    if re.fullmatch(r"\d+", entry):
        return Result.ok([int(entry)])

    # Single Range
    if re.fullmatch(r"\d+\s*-\s*\d+", entry):
        range_parts = entry.split(HYPHEN)
        start = int(range_parts[0].strip())
        end = int(range_parts[1].strip())
        if start >= end:
            return Result.err(f"Invalid range '{entry}': start must be less than end")
        return Result.ok(list(range(start, end + 1)))
    
    # Determine delimiter
    delimiter = COMMA if COMMA in entry else SEMI if SEMI in entry else None
    if delimiter is None:
        return Result.err(f"Invalid format: '{entry}'")
    
    # Split and process each part
    parts = [p.strip() for p in entry.split(delimiter) if p.strip()]
    values: list[int] = []
    
    for part in parts:
        # Single number
        if re.fullmatch(r"\d+", part):
            values.append(int(part))
        # Range
        elif re.fullmatch(r"\d+\s*-\s*\d+", part):
            range_parts = part.split(HYPHEN)
            start = int(range_parts[0].strip())
            end = int(range_parts[1].strip())
            if start >= end:
                return Result.err(f"Invalid range '{part}': start must be less than end")
            values.extend(range(start, end + 1))
        else:
            return Result.err(f"Invalid format in part: '{part}'")
    
    # Remove duplicates and sort
    return Result.ok(sorted(set(values)))
