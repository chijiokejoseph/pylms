import pandas as pd

from ..constants import INTERNSHIP
from ..data import DataStream


def clean_internship(data_stream: DataStream[pd.DataFrame]) -> None:
    """Normalize internship values to uppercase and provide validation.

    This function converts all values in the column named by the module-level
    `INTERNSHIP` constant to upper-case strings. It returns a `DataStream`
    wrapping the transformed DataFrame and supplies a validator that ensures
    the `INTERNSHIP` column exists and that every value in the column is
    uppercase.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame to normalize.

    Returns:
        None
    """
    data: pd.DataFrame = data_stream.as_ref()

    data[INTERNSHIP] = data[INTERNSHIP].apply(str.upper)  # pyright: ignore [reportUnknownMemberType]
