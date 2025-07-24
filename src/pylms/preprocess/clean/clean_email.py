from pylms.constants import EMAIL
from pylms.utils.data import DataStream
import pandas as pd


def clean_email(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    data: pd.DataFrame = data_stream()
    data[EMAIL] = data[EMAIL].apply(lambda x: x.lower().strip())
    return DataStream(data)
