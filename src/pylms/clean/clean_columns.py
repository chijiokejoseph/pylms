import re

import pandas as pd

from ..constants import COMPLETION, DATA_COLUMNS
from ..data import DataStream


def preprocess_col(col: str) -> str:
    """Normalize a single column name.

    If the provided column name matches the pattern for "nysc/siwes"
    (case-insensitive), this helper returns the standardized `COMPLETION`
    constant. Otherwise the column name is stripped of surrounding whitespace
    and converted to title case.

    Args:
        col (str): The original column name.

    Returns:
        str: The normalized column name.
    """
    match str(col):
        case _ if re.match(r"nysc\s*/\s*siwes", col, flags=re.IGNORECASE):
            return COMPLETION
        case _:
            return col.strip().title()


def clean_columns(data_stream: DataStream[pd.DataFrame]) -> None:
    """Normalize and filter DataFrame columns inside a DataStream.

    This function computes a mapping from normalized column names (via
    `preprocess_col`) to the original column names, applies the mapping to
    rename columns in place, and then drops any columns that are not listed
    in the module-level `DATA_COLUMNS`

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame to be processed.

    Returns:
        None
    """
    data = data_stream.as_ref()
    columns: list[str] = data.columns.tolist()
    col_mappings: dict[str, str] = {preprocess_col(col): col for col in columns}
    data.rename(columns=col_mappings, inplace=True)
    columns_to_drop: list[str] = [col for col in columns if col not in DATA_COLUMNS]
    data.drop(columns=columns_to_drop, inplace=True)
    return None
