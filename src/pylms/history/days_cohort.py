from datetime import datetime, timedelta
from typing import overload

from ..constants import WEEK_DAYS
from ..errors import Result, Unit, eprint
from .history import History


def update_dates(history: History) -> Result[Unit]:
    """
    Updates the dates based on the class dates and orientation date.

    This method calculates the dates for the classes based on the class dates and the orientation date.
    It generates a list of dates for the entire duration of the course, ensuring that only the
    weekdays specified in ``class_dates`` are included.

    :param history: (History) - The instance of the History class.
    :type history: History

    :return: Result[Unit]
    :rtype: Result[Unit]
    """
    # Validate that exactly three class weekdays are specified
    if len(history.class_days) != 3:
        msg = "Class days must contain exactly 3 integers corresponding to the weekdays on which classes are held."
        eprint(msg)
        return Result.err(msg)

    # Ensure the orientation date is set before proceeding
    if history.orientation_date is None:
        msg = "Orientation date must be set before updating dates."
        eprint(msg)
        return Result.err(msg)

    # Generate all dates for the course duration, starting from the day after orientation
    all_dates: list[datetime] = [
        history.orientation_date + timedelta(days=i)
        for i in range(1, 7 * history.weeks)
    ]

    # Identify the last date in the generated range
    last_date: datetime = all_dates[-1]

    # Calculate how many days remain in the final week to reach the next Sunday
    diff = 6 - last_date.weekday()

    # Generate the remaining dates to complete the final week
    dates_left: list[datetime] = [
        last_date + timedelta(days=i) for i in range(1, diff + 1)
    ]

    # Extend the list of all dates to include the remaining days in the final week
    all_dates.extend(dates_left)

    # Filter all dates to include only those that match the specified class weekdays
    history.dates = [date for date in all_dates if date.weekday() in history.class_days]

    return Result.unit()


@overload
def set_class_days(history: History, days: list[int], *, start: int) -> Result[Unit]:
    pass


@overload
def set_class_days(history: History, days: list[str], *, start: None) -> Result[Unit]:
    pass


def set_class_days(
    history: History,
    days: list[int] | list[str],
    *,
    start: int | None,
) -> Result[Unit]:
    """
    Sets the class days for the schedule.

    This method validates and sets the days of the week on which classes are held.
    The days parameter must contain exactly three unique elements, either as integers
    (weekday indices) or as strings (weekday names). If integers are provided, a start
    index must also be specified. If strings are provided, they must match entries in
    the WEEK_DAYS list.

    :param history: (History) - The instance of the History class.
    :type history: History
    :param days: (SupportsLenGetitem[int] | SupportsLenGetitem[str]) - A sequence of exactly 3 elements, each representing a weekday.
        If elements are integers, they represent weekday indices (e.g., 0 for Monday).
        If elements are strings, they must match entries in WEEK_DAYS (e.g., "Monday").
    :type days: SupportsLenGetitem[int] | SupportsLenGetitem[str]
    :param start: (int | None) - The starting weekday index. Required if `days` contains integers.
    :type start: int | None

    :return: (Result[Unit]) - returns a result object
    :rtype: Result[Unit]
    """
    # Ensure exactly three days are provided
    if len(days) != 3:
        msg = "Class days must contain exactly 3 integers corresponding to the weekdays on which classes are held."
        eprint(msg)
        return Result.err(msg)

    # Ensure all days are unique
    if days[0] == days[1] or days[0] == days[2] or days[1] == days[2]:
        msg = "Class days must contain unique integers corresponding to the weekdays on which classes are held."
        eprint(msg)
        return Result.err(msg)

    # Determine the type of input and process accordingly
    match True:
        # If integers are provided and a start index is given, calculate weekday indices
        case _ if all(isinstance(day, int) for day in days) and start is not None:
            days = [day for day in days if isinstance(day, int)]
            # Subtract start from each integer to normalize to weekday indices
            history.class_days = [i - start for i in days]

        # If strings are provided and all are valid weekday names, convert to indices
        case _ if all(isinstance(day, str) for day in days):
            days = [day for day in days if isinstance(day, str)]
            missing = [day for day in days if day.title() not in WEEK_DAYS]
            if len(missing) > 0:
                messages = [f"{day.title()}" for day in days]
                msg = ", ".join(messages) + f" not in {WEEK_DAYS}"
                eprint(msg)
                return Result.err(msg)

            # Map weekday names to their indices
            history.class_days = [WEEK_DAYS.index(day) for day in days]

        # If integers are provided but no start index, raise an error
        case _ if all(isinstance(day, int) for day in days) and start is None:
            msg = "Start must be provided if first is an integer."
            eprint(msg)
            return Result.err(msg)

        # If strings are provided but not all are valid weekday names, raise an error
        case _ if all(isinstance(day, str) for day in days) and not all(
            day in WEEK_DAYS for day in days
        ):
            msg = "Days must be a list of strings corresponding to the weekdays on which classes are held, and must match the following list {WEEK_DAYS}."
            eprint(msg)
            return Result.err(msg)

        # For any other invalid input, raise an error
        case _:
            msg = "Days must be a list of integers or strings corresponding to the weekdays on which classes are held, and must match the following list {WEEK_DAYS}."
            eprint(msg)
            return Result.err(msg)

    return Result.unit()


def extend_weeks(history: History, additional_weeks: int) -> Result[Unit]:
    """Extends the number of weeks in the history.

    :param additional_weeks: (int) - The number of additional weeks to extend.
    :type additional_weeks: int

    :return: (Result[Unit]) - a result object.
    :rtype: Result[Unit]


    """
    if additional_weeks < 0:
        msg = "Additional weeks must be a non-negative integer."
        eprint(msg)
        return Result.err(msg)
    history.weeks += additional_weeks
    return update_dates(history)


def replan_weeks(history: History, new_weeks: int) -> Result[Unit]:
    """Replans the number of weeks in the history.

    This method sets a new number of weeks for the course and updates the relevant dates
    based on the new duration.

    :param new_weeks: (int) - The new number of weeks for the course.
    :type new_weeks: int

    :return: (Result[Unit]) - a result object.
    :rtype: Result[Unit]


    """

    if new_weeks <= 1:
        msg = "Number of weeks must be greater than 1."
        eprint(msg)
        return Result.err(msg)

    history.weeks = new_weeks
    return update_dates(history)
