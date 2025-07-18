import pandas as pd
from datetime import datetime
from pylms.utils.data import DataStream
from pylms.utils.date import format_date
from pylms.constants import TIME_FMT, TIME


def _clean_time(entry: str | datetime) -> str:
    return format_date(entry, TIME_FMT)


def clean_time(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    data: pd.DataFrame = data_stream()
    data[TIME] = data[TIME].apply(_clean_time)
    return DataStream(data)
