import pandas as pd

from ..constants import UNIQUE_COLUMNS
from ..data import DataStream


def clean_duplicates_with_cols(
    data_stream: DataStream[pd.DataFrame], identifier_columns: list[str]
) -> DataStream[pd.DataFrame]:
    """removes duplicate rows from the underlying dataframe of the input parameter `data`

    :param data_stream: ( DataStream [pd.DataFrame] ): A DataStream object passed into the function
    :type data_stream: DataStream[pd.DataFrame]

    :param identifier_columns: ( list[str] ): A list of column names that will be used to determine duplicates in the `DataStream` object.
    :type identifier_columns: list[str]

    :return: DataStream instance with its underlying data formatted such that all duplicate rows have been removed.
    :rtype: DataStream[pd.DataFrame]
    """
    data: pd.DataFrame = data_stream()
    data.drop_duplicates(subset=identifier_columns, inplace=True)
    data.reset_index(drop=True, inplace=True)
    new_data: DataStream[pd.DataFrame] = DataStream(data)
    return new_data


def clean_duplicates(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    """removes duplicate rows from the underlying dataframe of the input parameter `data`

    :param data_stream: ( DataStream [pd.DataFrame] ): A DataStream object passed into the function
    :type data_stream: DataStream[pd.DataFrame]

    :return: DataStream instance with its underlying data formatted such that all duplicate rows have been removed.
    :rtype: DataStream[pd.DataFrame]
    """
    data: pd.DataFrame = data_stream().copy()
    data.drop_duplicates(subset=UNIQUE_COLUMNS, inplace=True)
    data.reset_index(drop=True, inplace=True)
    new_data: DataStream[pd.DataFrame] = DataStream(data)
    return new_data
