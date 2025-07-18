import pandas as pd

from pylms.utils.data import DataStream


def clean_duplicates(
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
    data: pd.DataFrame = data_stream().copy()
    for unique_col in identifier_columns:
        data = data.drop_duplicates(subset=[unique_col])
    data = data.reset_index(drop=True)
    new_data: DataStream[pd.DataFrame] = DataStream(data)
    return new_data
