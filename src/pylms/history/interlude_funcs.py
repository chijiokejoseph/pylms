from datetime import datetime

from ..constants import DATA_COLUMNS
from ..data import DataStore
from ..date import parse_dates
from ..errors import Result, Unit
from ..record import RecordStatus
from .classes import sync_classes
from .dates_with_history import all_dates
from .history import History
from .interlude import Interlude


def add_interlude(
    ds: DataStore, history: History, interlude: Interlude
) -> Result[Unit]:
    history.interlude = interlude

    result = sync_classes(history)
    if result.is_err():
        return result.propagate()
    _ = result.unwrap()

    new_dates = all_dates(history, datetime.now())
    new_start = new_dates.index(interlude.start)

    data = ds.as_ref()

    old_dates = [col for col in data.columns.tolist() if col not in DATA_COLUMNS]

    prev_dates = old_dates[new_start:]

    gap_dates = new_dates[new_start:]
    gap_dates = parse_dates(gap_dates).unwrap()

    del_dates: list[str] = []
    add_dates: list[str] = []

    diff = len(gap_dates) - len(prev_dates)
    if diff < 0:
        del_dates.extend(prev_dates[diff:])
        prev_dates = prev_dates[:diff]
    elif diff > 0:
        add_dates.extend(gap_dates[-diff:])
        gap_dates = gap_dates[:-diff]
    else:
        pass

    for date in del_dates:
        data.drop(date, inplace=True)

    for date in add_dates:
        data[date] = [RecordStatus.EMPTY for _ in range(data.shape[0])]

    for i, old in enumerate(prev_dates, start=1):
        data.rename(columns={old: i}, inplace=True)

    for i, new in enumerate(gap_dates, start=1):
        data.rename(columns={i: new}, inplace=True)

    return Result.unit()
