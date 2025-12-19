from datetime import datetime
from typing import overload

from ..constants import DATE_FMT
from ..errors import Result, eprint
from .history import History


def to_datetime(date_str: str) -> datetime | None:
    """Converts a date string to a datetime object.

    :param date_str: (str) - The date string to convert.
    :type date_str: str

    :return: (datetime) - The converted datetime object.
    :rtype: datetime


    """
    try:
        return datetime.strptime(date_str, DATE_FMT)
    except ValueError:
        msg = f"Invalid date format: {date_str}. Expected format is {DATE_FMT}."
        eprint(msg)
        return None


def parse_datetimes(dates_str: list[str]) -> Result[list[datetime]]:
    datetimes: list[datetime] = []
    for date_str in dates_str:
        value = to_datetime(date_str)
        if value is None:
            return Result.err("")
        datetimes.append(value)

    return Result.ok(datetimes)


@overload
def all_dates(history: History, sample: datetime) -> list[datetime]:
    pass


@overload
def all_dates(history: History, sample: str) -> list[str]:
    pass


def all_dates(history: History, sample: str | datetime) -> list[str] | list[datetime]:
    if isinstance(sample, datetime):
        return history.dates
    else:
        return [date.strftime(DATE_FMT) for date in history.dates]
