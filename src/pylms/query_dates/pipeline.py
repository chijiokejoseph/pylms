"""Pipeline for applying multiple date selectors."""

from ..errors import Result
from ..history import History
from .selector_type import DateSelector
from .sink import DateSink
from .sink_select import search_from_sink


def apply_selector_pipeline(
    history: History, selectors: list[DateSelector]
) -> Result[list[str]]:
    """Apply multiple date selectors and return intersection of results.

    Args:
        history (History): History instance containing class information.
        selectors (list[DateSelector]): List of selectors to apply.

    Returns:
        Result[list[str]]: Success with list of dates matching all selectors or error.
    """
    # Check for empty selectors list
    if len(selectors) == 0:
        return Result.err("No selectors provided")

    # Pop first selector to initialize sink
    first_selector = selectors[0]
    sink = DateSink.from_history(history, first_selector)
    if sink.is_err():
        return sink.propagate()

    sink = sink.unwrap()

    # Apply remaining selectors sequentially
    for selector in selectors:
        # Search from sink with current selector
        result = search_from_sink(history, sink, selector)
        if result.is_err():
            return result.propagate()

        # Update sink with narrowed results
        dates = result.unwrap()
        sink.dates = dates

    # Get final dates from sink
    dates = sink.dates
    
    # Check if any dates remain after all filters
    if len(dates) == 0:
        return Result.err("No dates match selected criteria")

    # Return sorted dates
    return Result.ok(sorted(dates))
