from datetime import datetime
from typing import overload

from ..constants import DATE_FMT
from .history import History


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
