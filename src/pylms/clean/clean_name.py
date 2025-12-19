import pandas as pd

from ..constants import COMMA_DELIM, NAME, SPACE_DELIM
from ..data import DataStream


def clean_name(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    """takes an input DataStream `data`, reads its underlying data and generates a new dataframe instance with the entries from the `NAME` column of the underlying data which are formatted using the function `_clean_name`. The new dataframe is returned as a new DataStream instance.

    :param data_stream: ( DataStream[pd.DataFrame] ): a DataStream object that contains the underlying data to be formatted
    :type data_stream: DataStream[pd.DataFrame]

    :return: a new DataStream instance which contains the formatted data as its underlying data.
    :rtype: DataStream[pd.DataFrame]
    """
    data: pd.DataFrame = data_stream().copy()
    data[NAME] = data[NAME].apply(_clean_name)  # pyright: ignore [reportUnknownMemberType]
    return DataStream(data)


def _clean_name(entry: str) -> str:
    """takes an input string `entry` and formats it such that its substrings separated by a whitespace are now separated by commas at the end of the operation.

    The designated target of this function is a string input of an individual's name. The function aims to properly format the input name to make it much easier to parse for future use.

    :param entry: ( str ): An input string of a person's name
    :type entry: str

    :return: formatted string with each distinct name in the input string separated by a comma and not a whitespace.
    :rtype: str
    """
    if entry.find(COMMA_DELIM) == -1:
        entries: list[str] = entry.split(SPACE_DELIM)
        entry = COMMA_DELIM.join(entries)
    entry = entry.title()
    return entry
