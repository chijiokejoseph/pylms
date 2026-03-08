"""General query function for date selection."""

from ..cli import input_str
from ..errors import ForcedExitError, Result
from ..history import History
from ..info import print_info
from .interactive import search_dates
from .pipeline import apply_selector_pipeline
from .query_parse import query_parse


def run_query_dates(history: History) -> Result[list[str]]:
    """General interactive function to query class dates.

    Prompts user for a query string with date selectors (held, unheld, marked, unmarked, weekday).
    Parses the query and applies selectors via pipeline. Loops until valid input or ForcedExitError.

    Args:
        history (History): History instance containing class information.

    Returns:
        Result[list[str]]: Success with list of selected dates or ForcedExitError.
    """
    # Define detailed prompt message
    prompt = """Enter query to select class dates:
  - Held: held
  - Unheld: unheld
  - Marked: marked
  - Unmarked: unmarked
  - Weekday: weekday
  - Combine: held, marked, weekday
Query: """

    # Loop until valid input or forced exit
    while True:
        # Prompt for query input
        result = input_str(
            prompt, lambda x: len(x.strip()) > 0, diagnosis="Query cannot be empty"
        )

        # Check for forced exit
        if result.is_err():
            err = result.unwrap_err()
            if isinstance(err, ForcedExitError):
                return result.propagate()
            result.print_if_err()
            continue

        # Parse query string
        query = result.unwrap()
        parse_result = query_parse(query)

        # Check parse result - if parsing fails, fall back to interactive search
        if parse_result.is_err():
            err = parse_result.unwrap_err()
            if isinstance(err, ForcedExitError):
                return parse_result.propagate()
            parse_result.print_if_err()
            print_info("Falling back to interactive search...\n")
            return search_dates(history)

        # Apply selector pipeline
        selectors = parse_result.unwrap()
        pipeline_result = apply_selector_pipeline(history, selectors)

        # Check pipeline result
        if pipeline_result.is_err():
            err = pipeline_result.unwrap_err()
            if isinstance(err, ForcedExitError):
                return pipeline_result.propagate()
            pipeline_result.print_if_err()
            continue

        # Return successful result
        return pipeline_result
