from datetime import datetime

import pandas as pd

from ..constants import TIME, TIME_FMT
from ..data import DataStream
from ..date import format_date


def _clean_time(entry: str | datetime) -> str:
    return format_date(entry, TIME_FMT)


def clean_time(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    data: pd.DataFrame = data_stream()
    data[TIME] = data[TIME].apply(_clean_time)  # pyright: ignore[reportUnknownMemberType]
    return DataStream(data)
