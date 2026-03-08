"""Interactive functions for user-driven date selection."""

from ..cli import input_option
from ..errors import Result
from ..history import History
from .pipeline import apply_selector_pipeline
from .search_held import search_held
from .search_marked import search_marked
from .search_unheld import search_unheld
from .search_unmarked import search_unmarked
from .search_weekday import search_weekday
from .selector_type import DateSelector


def search_dates(history: History) -> Result[list[str]]:
    """Interactive function to select dates using various search methods.
    
    Provides user with options to:
    1. Search held classes
    2. Search unheld classes
    3. Search marked classes
    4. Search unmarked classes
    5. Search by weekday
    6. Combined search (apply multiple filters)
    
    Args:
        history (History): History instance containing class information.
        
    Returns:
        Result[list[str]]: Success with list of selected dates or ForcedExitError.
    """
    # Define search method options
    options = [
        "Search held classes",
        "Search unheld classes",
        "Search marked classes",
        "Search unmarked classes",
        "Search by weekday",
        "Combined search (multiple filters)",
    ]
    
    # Display menu and get user selection
    result = input_option(options, prompt="How would you like to select dates?")
    if result.is_err():
        return result.propagate()
    
    # Extract selected index
    idx, _ = result.unwrap()
    
    # Delegate to appropriate search function
    match idx:
        case 1:
            return search_held(history)
        case 2:
            return search_unheld(history)
        case 3:
            return search_marked(history)
        case 4:
            return search_unmarked(history)
        case 5:
            return search_weekday(history)
        case 6:
            return combined_search(history)
        case _:
            return Result.err("Invalid selection")


def combined_search(history: History) -> Result[list[str]]:
    """Interactive combined search using multiple filters.
    
    Args:
        history (History): History instance containing class information.
        
    Returns:
        Result[list[str]]: Success with selected dates or ForcedExitError.
    """
    # Define filter options
    options = [
        "Held classes",
        "Unheld classes",
        "Marked classes",
        "Unmarked classes",
        "Weekday",
    ]
    
    # Map options to selectors
    selector_map = [
        DateSelector.HELD,
        DateSelector.UNHELD,
        DateSelector.MARKED,
        DateSelector.UNMARKED,
        DateSelector.WEEKDAY,
    ]
    
    # Collect selected filters
    selectors: list[DateSelector] = []
    
    # Loop to collect multiple filters
    while True:
        # Display menu and get filter selection
        result = input_option(options, prompt="Select a filter to add (or quit to finish)")
        if result.is_err():
            # If user quits and has selected filters, break to apply them
            if len(selectors) > 0:
                break
            # Otherwise propagate the error
            return result.propagate()
        
        # Extract selected index and add selector
        idx, _ = result.unwrap()
        selector = selector_map[idx]
        selectors.append(selector)

        # Remove conflicting options
        if selector == DateSelector.HELD:
            # Remove UNHELD option
            unheld_idx = selector_map.index(DateSelector.UNHELD)
            _ = options.pop(unheld_idx)
        
        if selector == DateSelector.UNHELD:
            # Remove HELD option
            held_idx = selector_map.index(DateSelector.HELD)
            _ = options.pop(held_idx)
        
        if selector == DateSelector.MARKED:
            # Remove UNMARKED option
            unmarked_idx = selector_map.index(DateSelector.UNMARKED)
            _ = options.pop(unmarked_idx)

        # Remove selected option from menu
        _ = options.pop(idx)
    
    # Check if any filters were selected
    if len(selectors) == 0:
        return Result.err("No filters selected")
    
    # Apply all selected filters via pipeline
    return apply_selector_pipeline(history, selectors)
