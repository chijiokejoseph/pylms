import pandas as pd

from ..constants import NAME, SERIAL
from ..data import DataStream


def clean_sort(data_stream: DataStream[pd.DataFrame]) -> None:
    """Sort rows by name and assign a 1-based serial number.

    Reads the DataFrame from `data_stream`, sorts it in-place by the column
    identified by the `NAME` constant, assigns a 1-based sequence to the
    `SERIAL` column and resets the DataFrame index.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame to sort and number.

    Returns:
        None
    """
    data: pd.DataFrame = data_stream.as_ref()
    data.sort_values(by=[NAME], inplace=True)
    data[SERIAL] = [i + 1 for i in range(data.shape[0])]
    data.reset_index(drop=True, inplace=True)
