from ..cli import select_class_date
from ..errors import Result
from ..history import History, get_unheld_classes


def input_class_date(history: History) -> Result[list[str]]:
    """Prompt user to select class dates for attendance form generation.
    
    Retrieves unheld class dates from history and allows user to select
    which dates to generate attendance forms for.
    
    Args:
        history (History): History instance to retrieve unheld class dates.
        
    Returns:
        Result[list[str]]: Success with selected dates or error message.
    """
    msg: str = "Attendance Form generation initiated. \nPlease enter the date(s) for which the form should be generated."
    dates: list[str] = [date for date in get_unheld_classes(history, "")]
    return select_class_date(msg, dates)
