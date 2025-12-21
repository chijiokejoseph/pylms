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
    """Converts a date string to a datetime object.

    :param date_str: (str) - The date string to convert.
    :type date_str: str

    :return: (datetime) - The converted datetime object.
    :rtype: datetime
    """
    try:
        if isinstance(date, str):
            return Result.ok(datetime.strptime(date, DATE_FMT))

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
    datetimes: list[datetime] = []
    dates_str: list[str] = []

    for date in dates:
        value = to_date(date)
        if value.is_err():
            return value.propagate()
        value = value.unwrap()
        if isinstance(value, datetime):
            datetimes.append(value)
        else:
            dates_str.append(value)

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
