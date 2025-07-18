from pylms.utils.data import DataStream
import pandas as pd
from pylms.constants import UNIQUE_COLUMNS


def clean_duplicates(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    """removes duplicate rows from the underlying dataframe of the input parameter `data`

    :param data_stream: ( DataStream [pd.DataFrame] ): A DataStream object passed into the function
    :type data_stream: DataStream[pd.DataFrame]

    :return: DataStream instance with its underlying data formatted such that all duplicate rows have been removed.
    :rtype: DataStream[pd.DataFrame]
    """
    data: pd.DataFrame = data_stream().copy()
    for unique_col in UNIQUE_COLUMNS:
        data = data.drop_duplicates(subset=[unique_col])
    data = data.reset_index(drop=True)
    new_data: DataStream[pd.DataFrame] = DataStream(data)
    return new_data
