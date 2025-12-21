import pandas as pd

from ..constants import DATA_COLUMNS
from ..data import DataStream


def clean_order(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    """Validate and reorder DataFrame columns according to the known schema.

    This function attaches a validator that ensures every column in the
    provided DataFrame is one of the expected `DATA_COLUMNS`. After validation
    it selects and returns the DataFrame with columns ordered as in
    `DATA_COLUMNS`, wrapped in a `DataStream`.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame to validate and reorder.

    Returns:
        DataStream[pd.DataFrame]: DataStream wrapping the DataFrame whose
            columns are ordered and validated against `DATA_COLUMNS`.
    """

    def validator(test_data: pd.DataFrame) -> bool:
        for col in test_data.columns:
            if col not in DATA_COLUMNS:
                return False
        return True

    valid_data: pd.DataFrame = DataStream(data_stream, validator)()
    valid_data = valid_data[DATA_COLUMNS]
    return DataStream(valid_data)
