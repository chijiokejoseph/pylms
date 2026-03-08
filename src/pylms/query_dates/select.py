from datetime import datetime

from ..constants import DATE_FMT
from ..errors import Result
from ..history import (
    History,
    all_dates,
    get_held_classes,
    get_marked_classes,
    get_unheld_classes,
    get_unmarked_classes,
)
from ..info import print_info
from .selector_type import DateSelector


def select(history: History, selector: DateSelector) -> Result[list[str]]:
    """Select dates from History based on DateSelector type.
    
    Args:
        history (History): History instance containing class information.
        selector (DateSelector): Type of date selection to perform.
        
    Returns:
        Result[list[str]]: Success with list of matching dates or error.
    """
    # Initialize empty values list
    values: list[str] = []
    
    # Match selector type and retrieve corresponding dates
    match selector:
        case DateSelector.HELD:
            # Get dates where classes were held
            values = get_held_classes(history, "")
        case DateSelector.UNHELD:
            # Get dates where classes were not held
            values = get_unheld_classes(history, "")
        case DateSelector.MARKED:
            # Get dates where attendance was marked
            values = get_marked_classes(history, "")
        case DateSelector.UNMARKED:
            # Get dates where attendance was not marked
            values = get_unmarked_classes(history, "")
        case DateSelector.WEEKDAY:
            # Get class days configuration
            class_days = history.class_days

            # Check if class days are configured
            if len(class_days) == 0:
                err_msg = "No class days configured in history"
                print_info(err_msg)
                return Result.err(err_msg)

            # Get all dates from history
            dates = all_dates(history, datetime.now())
            
            # Filter dates by weekday and convert to string format
            values = [
                date.strftime(DATE_FMT)
                for date in dates
                if date.weekday() in class_days
            ]

    return Result.ok(values)
