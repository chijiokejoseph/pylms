import pandas as pd

from ..constants import NAME, SERIAL
from ..data import DataStream


def clean_sort(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    data: pd.DataFrame = data_stream()
    data.sort_values(by=[NAME], inplace=True)
    data[SERIAL] = [i + 1 for i in range(data.shape[0])]
    data.reset_index(drop=True, inplace=True)
    return DataStream(data)
