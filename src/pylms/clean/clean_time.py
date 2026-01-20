from datetime import datetime

import numpy as np
import polars as pl

from pylms.data import datamap

from ..constants import TIME, TIME_FMT
from ..date import format_date


@np.vectorize
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


def clean_time(data: pl.DataFrame) -> pl.DataFrame:
    """Normalize the `TIME` column values in a pl.DataFrame's DataFrame.

    Applies the `_clean_time` helper to every entry in the column named by the
    `TIME` constant to produce a consistent, formatted time string for each
    row.

    Args:
        data (pl.DataFrame): The DataFrame whose `TIME` column should be normalized.

    Returns:
        pl.DataFrame: The processed DataFrame
    """
    return datamap(data, TIME, _clean_time, np.str_, pl.String())
