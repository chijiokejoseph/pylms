"""General query function for date selection."""

from ..cli import input_bool, input_str
from ..constants import COMMA
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
    prompt = """\nEnter query to select class dates:
  - Held: held
  - Unheld: unheld
  - Marked: marked
  - Unmarked: unmarked
  - Weekday: weekday
  - Combine: held, marked, weekday
  Press (Enter) to transition to interactive query
Query: """

    # Loop until valid input or forced exit
    while True:
        # Prompt for query input
        result = input_str(
            prompt, lambda x: len(x.strip()) > 0, diagnosis="Query cannot be empty"
        )

        # Check for forced exit
        if result.is_err() and isinstance(result.error, ForcedExitError):
            return result.propagate()
        elif result.is_err():
            result.print_if_err()
            continue

        # Parse query string
        query = result.unwrap()
        parse_result = query_parse(query)

        # Check parse result - if parsing fails, fall back to interactive search
        if parse_result.is_err() and isinstance(parse_result.error, ForcedExitError):
                return parse_result.propagate()
        elif parse_result.is_err():
            parse_result.print_if_err()
            print_info("Falling back to interactive search...\n")
            dates_result = search_dates(history)
            if dates_result.is_err():
                return dates_result.propagate()
            dates = dates_result.unwrap()
        else:
            # Apply selector pipeline
            selectors = parse_result.unwrap()
            pipeline_result = apply_selector_pipeline(history, selectors)

            # Check pipeline result
            if pipeline_result.is_err() and isinstance(
                pipeline_result.error, ForcedExitError
            ):
                return pipeline_result.propagate()
            elif pipeline_result.is_err():
                pipeline_result.print_if_err()
                continue

            dates = pipeline_result.unwrap()
        

        prompt = "Selected dates are: " + COMMA.join(dates)
        print_info(prompt)

        while True:
            choice = input_bool("Confirm selected dates")
            if choice.is_err() and isinstance(choice.error, ForcedExitError):
                return choice.propagate()
            elif choice.is_err():
                continue
            choice = choice.unwrap()
            if not choice:
                return Result.err("User quit operation")
            break
        # Return successful result
        return Result.ok(dates)
