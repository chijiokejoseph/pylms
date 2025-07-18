from pylms.utils.data import DataStream
from pylms.constants import NA_COLUMNS_FILL, TRAINING
from typing import cast
import pandas as pd


def clean_training(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    data: pd.DataFrame = data_stream()
    training_fill: str = cast(str, NA_COLUMNS_FILL[TRAINING])
    data[TRAINING] = training_fill
    return DataStream(data)
