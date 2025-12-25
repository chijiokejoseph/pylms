from collections.abc import Iterable
from typing import Any

import pandas as pd

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


def print_df(data: pd.DataFrame, serials: list[int]) -> None:
    """Pretty-print selected rows of a DataFrame.

    The function selects rows by 1-based serial numbers from `serials`, formats
    each selected row as a mapping of column-name -> value, and prints the
    entries with aligned columns for readability.

    Args:
        data (pd.DataFrame): The DataFrame to print from.
        serials (list[int]): A list of 1-based row indices indicating which
            rows to print.

    Returns:
        None

    Examples:
        >>> df = pd.DataFrame({'a': [1,2], 'b': ['x','y']})
        >>> print_df(df, [1])
        a : 1
        b : x
    """
    indices = [i - 1 for i in serials]
    subset = data.loc[indices, :]
    dataset = subset.to_dict(orient="records")  # pyright: ignore[reportUnknownMemberType]
    for entry in dataset:
        max_key = _max_print(entry.keys())
        max_value = _max_print(entry.values())
        for key, value in entry.items():
            print(f"{key:<{max_key}} : {value:<{max_value}}")
        print("\n")


def print_stream(stream: DataStream[pd.DataFrame], serials: list[int]) -> None:
    """Pretty-print rows from a `DataStream`-backed DataFrame.

    This is a thin wrapper around `print_df` that extracts the DataFrame from
    the provided `DataStream` and delegates printing.

    Args:
        stream (DataStream[pd.DataFrame]): DataStream wrapping the DataFrame.
        serials (list[int]): A list of 1-based row indices indicating which
            rows to print.

    Returns:
        None
    """
    print_df(stream(), serials)
