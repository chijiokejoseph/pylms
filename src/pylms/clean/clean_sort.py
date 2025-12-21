import pandas as pd

from ..constants import NAME, SERIAL
from ..data import DataStream


def clean_sort(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    """Sort rows by name and assign a 1-based serial number.

    Reads the DataFrame from `data_stream`, sorts it in-place by the column
    identified by the `NAME` constant, assigns a 1-based sequence to the
    `SERIAL` column, resets the DataFrame index, and returns the processed
    DataFrame wrapped in a `DataStream`.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame to sort and number.

    Returns:
        DataStream[pd.DataFrame]: A DataStream wrapping the sorted DataFrame
            with a `SERIAL` column containing 1-based row numbers.
    """
    data: pd.DataFrame = data_stream()
    data.sort_values(by=[NAME], inplace=True)
    data[SERIAL] = [i + 1 for i in range(data.shape[0])]
    data.reset_index(drop=True, inplace=True)
    return DataStream(data)
