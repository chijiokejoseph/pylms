from datetime import datetime, timedelta
from typing import overload

from ..constants import WEEK_DAYS
from ..errors import Result, Unit, eprint
from .history import History


def sync_classes(history: History) -> Result[Unit]:
    """Update class dates based on orientation date and class days.
    
    Calculates dates for classes based on class days and orientation date,
    generating a list of dates for the entire course duration. Handles
    interludes by splitting the course into pre and post-interlude periods.
    
    Args:
        history (History): History instance to update.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    # Validate exactly three class weekdays
    if len(history.class_days) != 3:
        msg = "Class days must contain exactly 3 integers corresponding to the weekdays on which classes are held."
        eprint(msg)
        return Result.err(msg)

    # Ensure orientation date is set
    if history.orientation_date is None:
        msg = "Orientation date must be set before updating dates."
        eprint(msg)
        return Result.err(msg)

    # Generate all dates starting from day after orientation
    dates = [
        history.orientation_date + timedelta(days=i)
        for i in range(1, 7 * history.weeks)
    ]

    # Complete the final week to Sunday
    last_date = dates[-1]
    diff = 6 - last_date.weekday()
    dates_left: list[datetime] = [
        last_date + timedelta(days=i) for i in range(1, diff + 1)
    ]
    dates.extend(dates_left)

    # Handle interlude if present
    interlude = history.interlude

    if interlude is None:
        # No interlude - filter by class weekdays
        history.dates = [date for date in dates if date.weekday() in history.class_days]
        history._updated = True  # pyright: ignore[reportPrivateUsage]
        return Result.unit()

    # Split course around interlude
    gap_start = interlude.start
    pre_dates = [date for date in dates if date <= gap_start]

    # Calculate remaining weeks after interlude
    held_days = (gap_start - pre_dates[0]).days
    held_weeks = held_days // 7
    if held_days % 7 != 0:
        held_weeks += 1

    rem_weeks = history.weeks - held_weeks
    gap_end = interlude.end

    # Generate post-interlude dates
    shifted_dates = [gap_end + timedelta(i) for i in range(7 * rem_weeks)]
    last_date = shifted_dates[-1]
    diff = 6 - last_date.weekday()
    dates_left = [last_date + timedelta(days=i) for i in range(1, diff + 1)]

    # Combine all dates and filter by class weekdays
    dates = pre_dates + shifted_dates + dates_left
    dates = [date for date in dates if date.weekday() in history.class_days]

    history.dates = dates
    history._updated = True  # pyright: ignore[reportPrivateUsage]
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
    """Set class days for the schedule.
    
    Validates and sets the days of the week on which classes are held.
    Days must contain exactly three unique elements, either as integers
    (weekday indices) or strings (weekday names).
    
    Args:
        history (History): History instance to update.
        days (list[int] | list[str]): Exactly 3 unique weekdays as integers or strings.
        start (int | None): Starting weekday index (required if days are integers).
        
    Returns:
        Result[Unit]: Success or error message.
    """
    # Ensure exactly three days
    if len(days) != 3:
        msg = "Class days must contain exactly 3 values corresponding to the weekdays on which classes are held."
        eprint(msg)
        return Result.err(msg)

    # Ensure all days are unique
    if days[0] == days[1] or days[0] == days[2] or days[1] == days[2]:
        msg = "Class days must contain unique integers corresponding to the weekdays on which classes are held."
        eprint(msg)
        return Result.err(msg)

    # Process based on input type
    match True:
        # Integer days with start index
        case _ if all(isinstance(day, int) for day in days) and start is not None:
            days = [day for day in days if isinstance(day, int)]
            history.class_days = [i - start for i in days]

        # String days (weekday names)
        case _ if all(isinstance(day, str) for day in days):
            days = [day for day in days if isinstance(day, str)]
            missing = [day for day in days if day.title() not in WEEK_DAYS]
            if len(missing) > 0:
                messages = [f"{day.title()}" for day in days]
                msg = ", ".join(messages) + f" not in {WEEK_DAYS}"
                eprint(msg)
                return Result.err(msg)
            history.class_days = [WEEK_DAYS.index(day) for day in days]

        # Integer days without start index
        case _ if all(isinstance(day, int) for day in days) and start is None:
            msg = "Start must be provided if first is an integer."
            eprint(msg)
            return Result.err(msg)

        # Invalid string days
        case _ if all(isinstance(day, str) for day in days) and not all(
            day in WEEK_DAYS for day in days
        ):
            msg = f"Days must be a list of strings corresponding to the weekdays on which classes are held, and must match the following list {WEEK_DAYS}."
            eprint(msg)
            return Result.err(msg)

        # Any other invalid input
        case _:
            msg = f"Days must be a list of integers or strings corresponding to the weekdays on which classes are held, and must match the following list {WEEK_DAYS}."
            eprint(msg)
            return Result.err(msg)

    return Result.unit()


def extend_weeks(history: History, additional_weeks: int) -> Result[Unit]:
    """Extend the number of weeks in the history.
    
    Args:
        history (History): History instance to update.
        additional_weeks (int): Number of additional weeks to extend.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    if additional_weeks < 1:
        msg = "Additional weeks must be a positive non-zero integer."
        eprint(msg)
        return Result.err(msg)
    history.weeks += additional_weeks
    return sync_classes(history)


def replan_weeks(history: History, new_weeks: int) -> Result[Unit]:
    """Replan the number of weeks in the history.
    
    Sets a new number of weeks for the course and updates relevant dates
    based on the new duration.
    
    Args:
        history (History): History instance to update.
        new_weeks (int): New number of weeks for the course.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    if new_weeks <= 1:
        msg = "Number of weeks must be greater than 1."
        eprint(msg)
        return Result.err(msg)

    history.weeks = new_weeks
    return sync_classes(history)
