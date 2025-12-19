import pandas as pd

from ..constants import DATA_COLUMNS
from ..data import DataStream


def clean_order(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    def validator(test_data: pd.DataFrame) -> bool:
        for col in test_data.columns:
            if col not in DATA_COLUMNS:
                return False
        return True

    valid_data: pd.DataFrame = DataStream(data_stream, validator)()
    valid_data = valid_data[DATA_COLUMNS]
    return DataStream(valid_data)
