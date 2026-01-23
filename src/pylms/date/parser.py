from datetime import datetime
from typing import overload

from ..constants import DATE_FMT
from ..errors import Result, eprint


@overload
def to_date(date: str) -> Result[datetime]:
    pass


@overload
def to_date(date: datetime) -> Result[str]:
    pass


def to_date(date: str | datetime) -> Result[datetime] | Result[str]:
    """Convert between date string and datetime object.
    
    Args:
        date (str | datetime): Date string in DATE_FMT format or datetime object.
        
    Returns:
        Result[datetime] | Result[str]: Success with converted value or error message.
    """
    try:
        if isinstance(date, str):
            # Convert string to datetime
            return Result.ok(datetime.strptime(date, DATE_FMT))

        # Convert datetime to string
        return Result.ok(date.strftime(DATE_FMT))
    except ValueError:
        msg = f"Invalid date format: {date}. Expected format is {DATE_FMT}."
        eprint(msg)
        return Result.err(msg)


@overload
def parse_dates(dates: list[str]) -> Result[list[datetime]]:
    pass


@overload
def parse_dates(dates: list[datetime]) -> Result[list[str]]:
    pass


def parse_dates(
    dates: list[str] | list[datetime],
) -> Result[list[datetime]] | Result[list[str]]:
    """Convert list of dates between string and datetime formats.
    
    Args:
        dates (list[str] | list[datetime]): List of date strings or datetime objects.
        
    Returns:
        Result[list[datetime]] | Result[list[str]]: Success with converted list or error.
        
    Note:
        All items in the list must be the same type (all strings or all datetimes).
    """
    datetimes: list[datetime] = []
    dates_str: list[str] = []

    # Convert each date and collect results
    for date in dates:
        value = to_date(date)
        if value.is_err():
            return value.propagate()
        value = value.unwrap()
        if isinstance(value, datetime):
            datetimes.append(value)
        else:
            dates_str.append(value)

    # Return appropriate result based on what was converted
    if len(datetimes) == 0 and len(dates_str) > 0:
        return Result.ok(dates_str)
    elif len(datetimes) > 0 and len(dates_str) == 0:
        return Result.ok(datetimes)
    elif len(datetimes) == 0 and len(dates_str) == 0:
        return Result.ok([])
    else:
        msg = "Invalid argument passed, argument `dates` can either be `list[str]` or `list[datetime]` not `list[str | datetime]`"
        eprint(msg)
        return Result.err(msg)
