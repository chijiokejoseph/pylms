from pylms.cli.select_class_date import select_class_date
from pylms.constants import DATE_FMT
from pylms.history import History


def input_class_date(history: History) -> list[str]:
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
    src_dates: list[str] = [
        date.strftime(DATE_FMT) for date in history.get_unheld_classes()
    ]
    return select_class_date(msg, src_dates_list=src_dates)
