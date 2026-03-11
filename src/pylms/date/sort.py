from datetime import datetime
from typing import cast, overload

from ..constants import DATE_FMT


def str_key(date: str) -> float:
    timestamp = datetime.strptime(date, DATE_FMT).timestamp()
    return timestamp


def date_key(date: datetime) -> float:
    return date.timestamp()


@overload
def sort_dates(dates: list[str]) -> list[str]:
    """
    Sort list of date strings.

    Args:
        dates (list[str]): List of date strings in DATE_FMT format.

    Returns:
        list[str]: Sorted list of date strings.
    """
    pass


@overload
def sort_dates(dates: list[datetime]) -> list[datetime]:
    """
    Sort list of datetime objects.

    Args:
        dates (list[datetime]): List of datetime objects.

    Returns:
        list[datetime]: Sorted list of datetime objects.
    """
    pass


def sort_dates(dates: list[str] | list[datetime]) -> list[str] | list[datetime]:
    if len(dates) == 0:
        return dates

    if all(isinstance(date, str) for date in dates):
        dates_str = cast(list[str], dates)
        dates_str.sort(key=str_key)
        return dates_str
    else:
        dates_dt = cast(list[datetime], dates)
        dates_dt.sort(key=date_key)
        return dates_dt
