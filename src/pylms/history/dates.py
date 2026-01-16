from datetime import datetime
from typing import overload

from ..errors import Result
from .dates_with_history import all_dates
from .new import load_history


@overload
def retrieve_dates(sample: str) -> Result[list[str]]:
    pass


@overload
def retrieve_dates(sample: datetime) -> Result[list[datetime]]:
    pass


def retrieve_dates(
    sample: str | datetime,
) -> Result[list[str]] | Result[list[datetime]]:
    history = load_history()
    if history.is_err():
        return history.propagate()

    history = history.unwrap()

    if isinstance(sample, datetime):
        return Result.ok(all_dates(history, sample))

    return Result.ok(all_dates(history, sample))
