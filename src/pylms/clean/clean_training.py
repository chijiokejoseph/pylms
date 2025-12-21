from typing import cast

import pandas as pd

from ..constants import NA_COLUMNS_FILL, TRAINING
from ..data import DataStream


def clean_training(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    """Fill the `TRAINING` column with the configured default value.

    This function obtains the DataFrame from the provided `DataStream`, looks
    up the default fill value for the `TRAINING` column from the
    `NA_COLUMNS_FILL` mapping, assigns that value to the entire `TRAINING`
    column, and returns the modified DataFrame wrapped in a `DataStream`.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame whose `TRAINING` column should be filled.

    Returns:
        DataStream[pd.DataFrame]: A DataStream wrapping the DataFrame with the
            `TRAINING` column set to the default fill value.
    """
    data: pd.DataFrame = data_stream()
    training_fill: str = cast(str, NA_COLUMNS_FILL[TRAINING])
    data[TRAINING] = training_fill
    return DataStream(data)
