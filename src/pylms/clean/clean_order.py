import pandas as pd

from ..constants import DATA_COLUMNS
from ..data import DataStream
from ..errors import Result


def clean_order(
    data_stream: DataStream[pd.DataFrame],
) -> Result[DataStream[pd.DataFrame]]:
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

    result = DataStream.verify(data_stream, validator)
    if result.is_err():
        return result.propagate()

    data = data_stream.as_ref()
    data = data[DATA_COLUMNS]
    return Result.ok(DataStream(data))
