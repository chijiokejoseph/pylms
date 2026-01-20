import numpy as np
import polars as pl

from ..data import datamap

from ..constants import ARABIC_APOSTROPHE, COMMA_DELIM, NAME, SPACE_DELIM


def clean_name(data: pl.DataFrame) -> pl.DataFrame:
    """Format the `NAME` column entries in a pl.DataFrame's DataFrame.

    Reads the DataFrame from `data`, applies the helper `_clean_name`
    to each value in the column identified by the `NAME` constant and mutates
    the DataFrame

    Args:
        data (pl.DataFrame): The DataFrame whose `NAME` column will be formatted.

    Returns:
        None
    """
    # name: np.ndarray = data[NAME].to_numpy()
    # name = _clean_name(name)
    # name = np.array(name, dtype=pl.String)
    # data = data.with_columns(
    #     pl.Series(NAME, data, dtype=pl.String)
    # )
    data = datamap(data, NAME, _clean_name, np.str_, pl.String())
    return data


@np.vectorize
def _clean_name(entry: str) -> str:
    """Normalize an individual's name string.

    If the entry contains no commas, whitespace-separated tokens are joined
    with the `COMMA_DELIM`. The result is then converted to title case.

    Args:
        entry (str): The input name string.

    Returns:
        str: The formatted name string.
    """
    if entry.find(COMMA_DELIM) == -1:
        entries: list[str] = entry.split(SPACE_DELIM)
        entry = COMMA_DELIM.join(entries)
    entry = entry.title()

    idx = entry.find(ARABIC_APOSTROPHE)

    if idx != -1:
        seq = entry[idx : idx + 2]
        entry = entry.replace(seq, seq.lower())
        entry = entry.capitalize()

    return entry
