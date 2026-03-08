"""Interactive function for selecting held class dates."""

from ..cli import input_dates
from ..errors import ForcedExitError, Result
from ..history import History, get_held_classes, match_classes
from ..info import print_info


def search_held(history: History) -> Result[list[str]]:
    """Interactive function to select held class dates.
    
    Displays menu and prompts user to enter class numbers for held classes.
    Loops until valid selection or ForcedExitError.
    
    Args:
        history (History): History instance containing class information.
        
    Returns:
        Result[list[str]]: Success with list of selected held dates or ForcedExitError.
    """
    # Loop until valid selection or forced exit
    while True:
        # Get held classes from history
        dates = get_held_classes(history, "")
        
        # Check if any held classes exist
        if len(dates) == 0:
            err_msg = "No held classes found"
            print_info(err_msg)
            return Result.err(err_msg)
        
        # Display menu and get user input
        result = input_dates(dates, "Select held class dates")
        if result.is_err():
            err = result.unwrap_err()
            # Check for forced exit
            if isinstance(err, ForcedExitError):
                return result.propagate()
            # Print error and continue loop
            result.print_if_err()
            continue

        # Parse user input to match classes
        entry = result.unwrap()
        
        return match_classes(history, entry, dates)
