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
    """Get all dates from history in specified format.
    
    Args:
        history (History): History instance containing dates.
        sample (str | datetime): Sample to determine return type.
        
    Returns:
        list[str] | list[datetime]: Dates as datetime objects or formatted strings.
    """
    if isinstance(sample, datetime):
        return history.dates
    else:
        return [date.strftime(DATE_FMT) for date in history.dates]
