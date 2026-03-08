from ..cli import input_dates
from ..errors import ForcedExitError, Result
from ..history import History, match_classes
from .select import select
from .selector_type import DateSelector
from .sink import DateSink


def select_from_sink(
    history: History, sink: DateSink, selector: DateSelector
) -> Result[list[str]]:
    """Select dates from a DateSink using intersection with selector results.
    
    Args:
        history (History): History instance containing class information.
        sink (DateSink): DateSink containing current filtered dates.
        selector (DateSelector): Selector to apply for intersection.
        
    Returns:
        Result[list[str]]: Success with intersected dates or error.
    """
    # Convert sink dates to set for intersection
    dates_set = set(sink.dates)
    
    # Get dates matching the selector
    matched = select(history, selector)
    if matched.is_err():
        return matched.propagate()
    matched = matched.unwrap()

    # Convert matched dates to set and perform intersection
    matched_set = set(matched)
    result = list(dates_set.intersection(matched_set))
    
    return Result.ok(result)


def search_from_sink(
    history: History, sink: DateSink, selector: DateSelector
) -> Result[list[str]]:
    """Search for dates from a DateSink with interactive user selection.
    
    Args:
        history (History): History instance containing class information.
        sink (DateSink): DateSink containing current filtered dates.
        selector (DateSelector): Selector to apply for intersection.
        
    Returns:
        Result[list[str]]: Success with selected dates or ForcedExitError.
    """
    # Loop until valid selection or forced exit
    while True:
        # Get intersection of sink dates and selector dates
        dates = select_from_sink(history, sink, selector)
        if dates.is_err():
            return dates.propagate()

        dates = dates.unwrap()

        # Display menu and get user input
        result = input_dates(dates, "Enter class date: ")
        if result.is_err():
            err = result.unwrap_err()
            # Check for forced exit
            if isinstance(err, ForcedExitError):
                return result.propagate()
            continue

        # Parse user input to match classes
        class_input = result.unwrap()
        match_result = match_classes(history, class_input, dates)
        if match_result.is_err():
            err = match_result.unwrap_err()
            # Check for forced exit
            if isinstance(err, ForcedExitError):
                return match_result.propagate()
            # Print error and continue loop
            match_result.print_if_err()
            continue

        # Return successful match
        return match_result
