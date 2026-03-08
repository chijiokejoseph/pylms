"""Parse query strings to extract search criteria."""

import re
from pathlib import Path

from pylms.query_data.select_path import select_path

from ..cli_utils import parse_nums
from ..data import DataStore
from ..errors import Result
from .select_completion import select_completion
from .select_gender import select_gender
from .select_internship import select_internship
from .select_name import select_name
from .select_serials import select_serials


def _process_token(ds: DataStore, token: str, serials: set[int]) -> None:
    """Process a single query token and update the serials set.

    Args:
        ds (DataStore): DataStore containing student data.
        token (str): Single token to process.
        serials (set[int]): Set to update with matching serial numbers.
    """
    match True:
        case _ if re.fullmatch(r"[\d,;\s-]+", token):
            # Serial numbers pattern
            result = parse_nums(token)
            if result.is_err():
                return
            nums = result.unwrap()
            serial_result = select_serials(ds, nums)
            if serial_result.is_err():
                return
            tuples = serial_result.unwrap()
            serials.update(s for s, _ in tuples)

        case _ if re.fullmatch(
            r'[a-zA-Z]:\\[^<>:"|?*]+|/[^<>:"|?*]+|\.\.?[/\\][^<>:"|?*]+|[^/\\<>:"|?*]+\.(txt|csv|xlsx)',
            token,
            re.IGNORECASE,
        ):
            # File path pattern (Windows/Unix absolute/relative paths with extensions)
            path = Path(token)
            if not path.exists():
                return
            if not path.is_file():
                return

            # Read serial numbers from file
            result = select_path(ds, path)
            if result.is_err():
                return
            tuples = result.unwrap()
            serials.update(s for s, _ in tuples)
            return

        case _ if re.fullmatch(r"nysc|siwes", token, re.IGNORECASE):
            # Internship category pattern
            category = token.upper()
            result = select_internship(ds, category)
            if result.is_err():
                return
            tuples = result.unwrap()
            serials.update(s for s, _ in tuples)

        case _ if re.fullmatch(r"m|f|male|female", token, re.IGNORECASE):
            # Gender pattern
            gender_map = {"m": "M", "f": "F", "male": "M", "female": "F"}
            gender = gender_map[token.lower()]
            result = select_gender(ds, gender)
            if result.is_err():
                return
            tuples = result.unwrap()
            serials.update(s for s, _ in tuples)

        case _ if re.fullmatch(
            r"january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec",
            token,
            re.IGNORECASE,
        ):
            # Completion month pattern
            result = select_completion(ds, token)
            if result.is_err():
                return
            tuples = result.unwrap()
            serials.update(s for s, _ in tuples)

        case _:
            # Default to name search
            result = select_name(ds, token)
            if result.is_err():
                return
            tuples = result.unwrap()
            serials.update(s for s, _ in tuples)


def query_parse(ds: DataStore, query: str) -> Result[list[int]]:
    """Parse query string and return matching student serial numbers.

    Parses a query string separated by commas or semicolons. Each token is classified as:
    - Serial numbers if it contains only digits and delimiters
    - File path if it matches a valid path pattern with .txt, .csv, or .xlsx extension
    - Internship if it matches "nysc" or "siwes" (case-insensitive)
    - Gender if it matches "m", "f", "male", or "female" (case-insensitive)
    - Completion date if it matches a valid month name
    - Name if none of the above patterns match

    All matching students from all tokens are combined (union operation).

    Args:
        ds (DataStore): DataStore containing student data.
        query (str): Query string with comma or semicolon separated tokens.

    Returns:
        Result[list[int]]: Success with list of matching serial numbers or error.
    """
    # Split query by commas or semicolons
    tokens = re.split(r"[,;]", query)
    tokens = [t.strip() for t in tokens if len(t.strip()) > 0]

    # Check for empty query
    if len(tokens) == 0:
        return Result.err("Empty query")

    # Process all tokens
    all_serials: set[int] = set()

    for token in tokens:
        _process_token(ds, token, all_serials)

    # Check if any students matched
    if len(all_serials) == 0:
        return Result.err("No students matched the query")

    return Result.ok(sorted(list(all_serials)))
