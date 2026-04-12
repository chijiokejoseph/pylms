"""Interactive query function for student selection."""

from ..cli import input_str
from ..data import DataStore
from ..errors import ForcedExitError, Result
from ..info import print_info
from .interactive import search_data
from .query_parse import query_parse


def run_query_data(ds: DataStore) -> Result[list[int]]:
    """Interactive function to query students using natural language input.

    Prompts user to enter a query string that can contain:
    - Serial numbers (e.g., "1,2,3" or "1-5")
    - Names (e.g., "John Doe")
    - Internship categories (e.g., "nysc", "siwes")
    - Gender (e.g., "m", "f", "male", "female")
    - Completion dates (e.g., "january", "feb")
    - File paths (e.g., "data.txt", "C:\\serials.xlsx")

    Multiple criteria can be combined using commas or semicolons.
    Loops until valid input or ForcedExitError.

    Args:
        ds (DataStore): DataStore containing student data.

    Returns:
        Result[list[int]]: Success with list of matching serial numbers or ForcedExitError.
    """
    # Define detailed prompt message
    prompt = """Enter query to select students:
  - Serials: 1,2,3 or 1-5
  - Names: John Doe
  - Category: nysc, siwes
  - Gender: m, f, male, female
  - Month: january, feb
  - File: path/to/file.txt, data.xlsx
  - Combine: John, 1-5, nysc, data.txt
  Press (Enter) to switch to interactive query
Query: """

    # Loop until valid input or forced exit
    while True:
        # Get user input
        result = input_str(prompt)
        if result.is_err() and isinstance(result.error, ForcedExitError):
            return result.propagate()
        elif result.is_err():
            continue

        # Parse query string
        query = result.unwrap()
        parse_result = query_parse(ds, query)

        # Check parse result - if parsing fails, fall back to interactive search
        if parse_result.is_err() and isinstance(parse_result.error, ForcedExitError):
            return parse_result.propagate()
        elif parse_result.is_err():
            # Print error and fall back to interactive search
            parse_result.print_if_err()
            print_info("Falling back to interactive search...\n")
            parse_result = search_data(ds)

        if parse_result.is_err() and isinstance(parse_result.error, ForcedExitError):
            return parse_result.propagate()
        elif parse_result.is_err():
            parse_result.print_if_err()
            return parse_result.propagate()

        # Return successful result
        return parse_result
