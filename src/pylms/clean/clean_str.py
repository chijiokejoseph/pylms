from typing import Any

import numpy as np
import polars as pl

from pylms.data import datamap

from ..constants import NA


def str_conv(entry: Any, default: str) -> str:
    """convert entry to python strings

    Args:
        entry (Any): any value
        default (str): the default to use in the hypothetical 
            case that string converstion fails

    Returns:
        str: string form of `entry` or default if the string
            conversion should actually fail
    """
    try:
        return str(entry)
    except ValueError:
        return default


def clean_str(
    data: pl.DataFrame,
    target_cols: str | list[str],
    fill: str = NA,
) -> pl.DataFrame:
    """Ensure specified DataFrame columns contain string values.

    Converts non-string entries in the specified column(s) to strings using
    the `_clean_str` helper. If an element cannot be converted it will be
    replaced with the provided `fill` value. `target_cols` may be either a
    single column name or a list of column names.

    Args:
        data (pl.DataFrame): The
            DataFrame to process.
        target_cols (str | list[str]): Column name or list of column names to
            normalize to strings.
        fill (str): String used to replace elements that cannot be converted.

    Returns:
        None
    """

    def _clean_str(entry: Any):
        return str_conv(entry, fill)

    if isinstance(target_cols, str):
        data = datamap(
            data, target_cols, np.vectorize(_clean_str), np.str_, pl.String()
        )
    else:
        for col in target_cols:
            data = datamap(data, col, np.vectorize(_clean_str), np.str_, pl.String())

    return data
