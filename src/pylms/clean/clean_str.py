from typing import Any

import pandas as pd

from ..constants import NA
from ..data import DataStream


def _clean_str(data: pd.Series, fill: str) -> pd.Series:
    """Convert series entries to strings, using `fill` for failures.

    Helper that ensures every element in `data` is represented as a string.
    If an element is already a `str` it is preserved; otherwise the function
    attempts to convert the element using `str()`. If conversion raises a
    `ValueError`, the provided `fill` value is used instead.

    Args:
        data (pd.Series): Series whose elements should be normalized to
            strings.
        fill (str): Replacement string to use when conversion fails.

    Returns:
        pd.Series: A new Series where every element is a string.
    """

    def str_conv(entry: Any, default: str) -> str:
        try:
            return str(entry)
        except ValueError:
            return default

    new_value: list[str] = [
        item if isinstance(item, str) else str_conv(item, fill)
        for item in data.tolist()
    ]
    return pd.Series(new_value)


def clean_str(
    data_stream: DataStream[pd.DataFrame],
    target_cols: str | list[str],
    fill: str = NA,
) -> None:
    """Ensure specified DataFrame columns contain string values.

    Converts non-string entries in the specified column(s) to strings using
    the `_clean_str` helper. If an element cannot be converted it will be
    replaced with the provided `fill` value. `target_cols` may be either a
    single column name or a list of column names.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame to process.
        target_cols (str | list[str]): Column name or list of column names to
            normalize to strings.
        fill (str): String used to replace elements that cannot be converted.

    Returns:
        None
    """

    data: pd.DataFrame = data_stream.as_ref()
    if isinstance(target_cols, str):
        data[target_cols] = _clean_str(data[target_cols], fill)
    else:
        for col in target_cols:
            data[col] = _clean_str(data[col], fill)
