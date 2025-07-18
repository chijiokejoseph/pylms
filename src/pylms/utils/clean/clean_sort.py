from pylms.utils.data import DataStream
from pylms.constants import NAME, SERIAL
import pandas as pd


def clean_sort(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    data: pd.DataFrame = data_stream()
    data = data.sort_values(by=[NAME])
    data[SERIAL] = [i + 1 for i in range(data.shape[0])]
    data = data.reset_index(drop=True)
    return DataStream(data)
