"""Interactive function for selecting marked class dates."""

from ..cli import input_dates
from ..errors import ForcedExitError, Result
from ..history import History, get_marked_classes, match_classes
from ..info import print_info


def search_marked(history: History) -> Result[list[str]]:
    """Interactive function to select marked class dates.
    
    Displays menu and prompts user to enter class numbers for marked classes.
    Loops until valid selection or ForcedExitError.
    
    Args:
        history (History): History instance containing class information.
        
    Returns:
        Result[list[str]]: Success with list of selected marked dates or ForcedExitError.
    """
    # Loop until valid selection or forced exit
    while True:
        # Get marked classes from history
        dates = get_marked_classes(history, "")
        
        # Check if any marked classes exist
        if len(dates) == 0:
            err_msg = "No marked classes found"
            print_info(err_msg)
            return Result.err(err_msg)
        
        # Display menu and get user input
        result = input_dates(dates, "Select marked class dates")
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
