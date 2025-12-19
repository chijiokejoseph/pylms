import pandas as pd

from ..constants import EMAIL
from ..data import DataStream


def clean_email(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    data: pd.DataFrame = data_stream()

    def apply(x: str) -> str:
        return x.lower().strip()

    data[EMAIL] = data[EMAIL].apply(apply)  # pyright: ignore [reportUnknownMemberType]
    return DataStream(data)
