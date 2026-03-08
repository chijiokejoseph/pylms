from datetime import datetime

import polars as pl

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
    """Add interlude to history and update DataStore dates accordingly.

    Updates the history with the interlude period and adjusts the DataStore
    columns to match the new date schedule, handling column additions,
    deletions, and renames as needed.

    Args:
        ds (DataStore): DataStore to update with new date columns.
        history (History): History instance to add interlude to.
        interlude (Interlude): Interlude period to add.

    Returns:
        Result[Unit]: Success or error message.
    """
    history.interlude = interlude

    # Sync classes with new interlude
    result = sync_classes(history)
    if result.is_err():
        return result.propagate()
    _ = result.unwrap()

    # Get new dates and find interlude start position
    new_dates = all_dates(history, datetime.now())
    new_start = new_dates.index(interlude.start)

    data = ds.as_ref()

    # Get existing date columns (excluding data columns)
    old_dates = [col for col in data.columns if col not in DATA_COLUMNS]

    # Get dates from interlude start onwards
    prev_dates = old_dates[new_start:]
    gap_dates = new_dates[new_start:]
    gap_dates = parse_dates(gap_dates).unwrap()

    # Calculate differences and prepare column operations
    del_dates: list[str] = []
    add_dates: list[str] = []

    diff = len(gap_dates) - len(prev_dates)
    if diff < 0:
        # More old dates than new - need to delete some
        del_dates.extend(prev_dates[diff:])
        prev_dates = prev_dates[:diff]
    elif diff > 0:
        # More new dates than old - need to add some
        add_dates.extend(gap_dates[-diff:])
        gap_dates = gap_dates[:-diff]

    # Update DataStore with new column structure
    data_updated = data

    # Remove excess columns
    if len(del_dates) > 0:
        data_updated = data_updated.drop(del_dates)

    # Add new columns with empty status
    for date in add_dates:
        data_updated = data_updated.with_columns(
            pl.lit(str(RecordStatus.EMPTY)).alias(date)
        )

    # Rename columns to match new dates
    rename_map = {}
    for old, new in zip(prev_dates, gap_dates):
        if old != new:
            rename_map[old] = new

    if len(rename_map) > 0:
        data_updated = data_updated.rename(rename_map)

    # Update DataStore with modified data
    return ds.copy_from(data_updated)
