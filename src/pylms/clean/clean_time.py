from datetime import datetime

import pandas as pd

from ..constants import TIME, TIME_FMT
from ..data import DataStream
from ..date import format_date


def _clean_time(entry: str | datetime) -> str:
    """Format a single time entry according to the project's time format.

    Helper that formats a single time value (either a `datetime` or a string
    parseable by the project's `format_date` helper) using the module-level
    `TIME_FMT` constant.

    Args:
        entry (str | datetime): The time value to format.

    Returns:
        str: The formatted time string according to `TIME_FMT`.
    """
    return format_date(entry, TIME_FMT)


def clean_time(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    """Normalize the `TIME` column values in a DataStream's DataFrame.

    Applies the `_clean_time` helper to every entry in the column named by the
    `TIME` constant to produce a consistent, formatted time string for each
    row. The resulting DataFrame is returned wrapped in a `DataStream`.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame whose `TIME` column should be normalized.

    Returns:
        DataStream[pd.DataFrame]: A DataStream wrapping the DataFrame with the
            `TIME` column normalized.
    """
    data: pd.DataFrame = data_stream()
    data[TIME] = data[TIME].apply(_clean_time)  # pyright: ignore[reportUnknownMemberType]
    return DataStream(data)
