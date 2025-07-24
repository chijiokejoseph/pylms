from typing import Any
from pylms.utils.data import DataStream
import pandas as pd
from pylms.constants import NA


def _clean_str(data: pd.Series, fill: str) -> pd.Series:
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
) -> DataStream[pd.DataFrame]:
    """
    clean a pandas series that is expected to contain only string data and replace all

    :param data_stream: ( DataStream[pd.Series] ): a `DataStream` instance to be cleaned
    :type data_stream: DataStream[pd.Series]
    :param target_cols: ( str | list[str] ): a single string containing the name of a column which is expected to hold string data to apply this formatting to or a list of names of such columns.
    :type target_cols: str | list[str]
    :param fill: ( str ): string value to be used to replace any entry in the underlying data of the `DataStream` instance passed as the argument to `data` that is not of the string data type.
    :type fill: str

    :return: cleaned data stored in a `DataStream` object
    :rtype: DataStream[pd.DataFrame]
    """
    data: pd.DataFrame = data_stream()
    if isinstance(target_cols, str):
        data[target_cols] = _clean_str(data[target_cols], fill)
    else:
        for col in target_cols:
            data[col] = _clean_str(data[col], fill)
    return DataStream(data)
