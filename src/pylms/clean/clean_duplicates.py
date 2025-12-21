import pandas as pd

from ..constants import UNIQUE_COLUMNS
from ..data import DataStream


def clean_duplicates_with_cols(
    data_stream: DataStream[pd.DataFrame], identifier_columns: list[str]
) -> DataStream[pd.DataFrame]:
    """Remove duplicate rows from a DataStream using specified columns.

    This function removes duplicate rows from the DataFrame contained in the
    provided `DataStream` by using the supplied `identifier_columns` to
    determine row uniqueness. The resulting DataFrame has its index reset and
    is returned wrapped in a `DataStream`.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame to deduplicate.
        identifier_columns (list[str]): Column names used to identify duplicate
            rows.

    Returns:
        DataStream[pd.DataFrame]: A DataStream wrapping the deduplicated DataFrame.
    """
    data: pd.DataFrame = data_stream()
    data.drop_duplicates(subset=identifier_columns, inplace=True)
    data.reset_index(drop=True, inplace=True)
    new_data: DataStream[pd.DataFrame] = DataStream(data)
    return new_data


def clean_duplicates(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    """Remove duplicate rows from a DataStream using the default schema.

    Removes duplicate rows from the DataFrame contained in `data_stream`
    using the module-level `UNIQUE_COLUMNS` list to determine uniqueness.
    The deduplicated DataFrame has its index reset and is returned wrapped in
    a `DataStream`.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame to deduplicate.

    Returns:
        DataStream[pd.DataFrame]: A DataStream wrapping the deduplicated DataFrame.
    """
    data: pd.DataFrame = data_stream().copy()
    data.drop_duplicates(subset=UNIQUE_COLUMNS, inplace=True)
    data.reset_index(drop=True, inplace=True)
    new_data: DataStream[pd.DataFrame] = DataStream(data)
    return new_data
