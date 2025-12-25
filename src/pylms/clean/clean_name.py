import pandas as pd

from ..constants import ARABIC_APOSTROPHE, COMMA_DELIM, NAME, SPACE_DELIM
from ..data import DataStream


def clean_name(data_stream: DataStream[pd.DataFrame]) -> None:
    """Format the `NAME` column entries in a DataStream's DataFrame.

    Reads the DataFrame from `data_stream`, applies the helper `_clean_name`
    to each value in the column identified by the `NAME` constant and mutates
    the DataFrame

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame whose `NAME` column will be formatted.

    Returns:
        None
    """
    data: pd.DataFrame = data_stream().copy()
    data[NAME] = data[NAME].apply(_clean_name)  # pyright: ignore [reportUnknownMemberType]


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
