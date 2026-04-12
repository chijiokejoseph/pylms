from collections.abc import Iterable
from typing import Any

import polars as pl

from ..constants import EMAIL, NAME, SERIAL
from .datastore import DataStore
from .datastream import DataStream


def _max_print(items: Iterable[Any]) -> int:
    """Return the length of the longest string representation in `items`.

    This helper computes the maximum width (in characters) required to render
    any element from the provided iterable when converted to string. It is
    primarily used to align key/value columns for pretty printing.

    Args:
        items (Iterable[Any]): Iterable of items to measure.

    Returns:
        int: The maximum length of the string representations of the items.

    Examples:
        >>> _max_print(['a', 'bb', 'ccc'])
        3
    """
    return max([len(str(item)) for item in items])


def print_df(data: pl.DataFrame, serials: list[int]) -> None:
    """Pretty-print selected rows of a DataFrame.

    The function selects rows by 1-based serial numbers from `serials`, formats
    each selected row as a mapping of column-name -> value, and prints the
    entries with aligned columns for readability.

    Args:
        data (pl.DataFrame): The DataFrame to print from.
        serials (list[int]): A list of 1-based row indices indicating which
            rows to print.

    Returns:
        None

    Examples:
        >>> df = pl.DataFrame({'a': [1,2], 'b': ['x','y']})
        >>> print_df(df, [1])
        a : 1
        b : x
    """
    indices = [i - 1 for i in serials]
    subset = data[indices]

    dataset = subset.to_dicts()
    for entry in dataset:
        max_key = _max_print(entry.keys())
        max_value = _max_print(entry.values())
        for key, value in entry.items():
            value = str(value)
            print(f"{key:<{max_key}} : {value:<{max_value}}")
        print("\n")


def print_stream(stream: DataStream, serials: list[int]) -> None:
    """Pretty-print rows from a `DataStream`-backed DataFrame.

    This is a thin wrapper around `print_df` that extracts the DataFrame from
    the provided `DataStream` and delegates printing.

    Args:
        stream (DataStream): DataStream wrapping the DataFrame.
        serials (list[int]): A list of 1-based row indices indicating which
            rows to print.

    Returns:
        None
    """
    print_df(stream.as_ref(), serials)


def print_ds_subset(ds: DataStore, serials: list[int]) -> None:
    display = (
        ds.pretty().filter(pl.col(SERIAL).is_in(serials)).select([SERIAL, NAME, EMAIL])
    )
    print()
    if len(serials) < 10:
        print(display)
        return

    with pl.Config(tbl_rows=-1, tbl_formatting="UTF8_FULL"):
        print(display)


def print_ds(ds: DataStore) -> None:
    display = ds.pretty().select([SERIAL, NAME, EMAIL])
    with pl.Config(tbl_rows=-1, tbl_formatting="UTF8_FULL"):
        print(display)
