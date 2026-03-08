"""Interactive function for selecting dates by weekday."""

from datetime import datetime

from pylms.cli_utils.nums import parse_nums

from ..cli import input_bool, input_dates, input_menu
from ..constants import DATE_FMT, WEEK_DAYS
from ..errors import ForcedExitError, Result
from ..history import History, all_dates, match_classes
from ..info import print_info


def search_weekday(history: History) -> Result[list[str]]:
    """Interactive function to select dates by weekday.

    Prompts user to select a weekday from class days in history,
    then displays menu and prompts to enter class numbers from dates on that weekday.
    Loops until valid selection or ForcedExitError.

    Args:
        history (History): History instance containing class information.

    Returns:
        Result[list[str]]: Success with list of selected dates or ForcedExitError.
    """
    # Loop until valid selection or forced exit
    while True:
        # Get class days from history
        class_days = history.class_days

        # Check if class days are configured
        if len(class_days) == 0:
            err_msg = "No class days configured in history"
            print_info(err_msg)
            return Result.err(err_msg)

        # Create options from class days
        options = [WEEK_DAYS[day] for day in class_days]

        # Display menu and get weekday selection
        result = input_menu(options, prompt="Select a weekday")
        if result.is_err():
            err = result.unwrap_err()
            # Check for forced exit
            if isinstance(err, ForcedExitError):
                return result.propagate()
            continue

        # Parse user input to get weekday indices
        entry = result.unwrap()
        idxs = parse_nums(entry)
        if idxs.is_err():
            continue

        # Convert indices to weekday numbers
        idxs = idxs.unwrap()
        weekdays = [class_days[idx - 1] for idx in idxs]
        weekdays_print = ", ".join([WEEK_DAYS[day] for day in weekdays])

        # Confirm weekday selection with user
        print_info(f"Selected weekdays: {weekdays_print}\n")
        result = input_bool("Confirm these days?")
        if result.is_err():
            err = result.unwrap_err()
            # Check for forced exit
            if isinstance(err, ForcedExitError):
                return result.propagate()
            continue
        
        # Check if user confirmed
        confirm = result.unwrap()
        if not confirm:
            continue

        # Get all dates as datetime objects
        dates_dt: list[datetime] = all_dates(history, datetime.now())

        # Filter dates by selected weekdays
        filtered_dt = [date for date in dates_dt if date.weekday() in weekdays]

        # Check if any dates match the weekdays
        if len(filtered_dt) == 0:
            err_msg = f"No classes found on {weekdays_print}"
            print_info(err_msg)
            continue

        # Convert datetime objects to string format
        filtered_dates = [date.strftime(DATE_FMT) for date in filtered_dt]

        # Display menu and get date selection
        result = input_dates(filtered_dates)
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
        return match_classes(history, entry, filtered_dates)
