from ..cli import select_class_date
from ..errors import Result
from ..history import History, get_unheld_classes


def input_class_date(history: History) -> Result[list[str]]:
    """
    Prompts the user to input class dates for which attendance forms should be generated.

    This function retrieves the list of unheld class dates from the history
    and prompts the user to select from these dates using the provided message.

    :param history: (History) - An instance of the History class to retrieve unheld class dates.
    :type history: History

    :return: (list[str]) - A list of selected class dates as strings in the specified date format.
    :rtype: list[str]
    """

    msg: str = "Attendance Form generation initiated. \nPlease enter the date(s) for which the form should be generated."
    src_dates: list[str] = [date for date in get_unheld_classes(history, "")]
    return select_class_date(msg, src_dates)
