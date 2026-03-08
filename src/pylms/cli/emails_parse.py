"""Parse query strings to determine email input type."""

import re
from pathlib import Path

from ..errors import Result
from .emails_mode import EmailInputMode


def query_emails_parse(query: str) -> Result[tuple[EmailInputMode, Path | str]]:
    """Parse query string to determine email input type and extract value.

    Patterns:
    - .txt file path -> TXT_FILE
    - .csv file path -> CSV_FILE
    - .xlsx/.xls file path -> EXCEL_FILE
    - Comma/semicolon delimited string -> RAW_STRING

    Args:
        query: Query string containing file path or email list.

    Returns:
        Result[tuple[EmailInputType, Path | str]]: Input type and value (path or string).
    """
    query = query.strip()

    if len(query) == 0:
        return Result.err("Empty query")

    # Check for file paths
    if re.search(r"\.txt$", query, re.IGNORECASE):
        path = Path(query)
        if not path.exists():
            return Result.err(f"File not found: {query}")
        return Result.ok((EmailInputMode.TXT, path))

    if re.search(r"\.csv$", query, re.IGNORECASE):
        path = Path(query)
        if not path.exists():
            return Result.err(f"File not found: {query}")
        return Result.ok((EmailInputMode.CSV, path))

    if re.search(r"\.(xlsx|xls)$", query, re.IGNORECASE):
        path = Path(query)
        if not path.exists():
            return Result.err(f"File not found: {query}")
        return Result.ok((EmailInputMode.EXCEL, path))

    # Default to raw string input
    return Result.ok((EmailInputMode.STRING, query))
