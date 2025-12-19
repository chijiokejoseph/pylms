from typing import cast

import pandas as pd

from ..constants import NA_COLUMNS_FILL, TRAINING
from ..data import DataStream


def clean_training(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    data: pd.DataFrame = data_stream()
    training_fill: str = cast(str, NA_COLUMNS_FILL[TRAINING])
    data[TRAINING] = training_fill
    return DataStream(data)
