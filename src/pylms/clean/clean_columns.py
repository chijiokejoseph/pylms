import re

import polars as pl

from ..constants import COMPLETION, DATA_COLUMNS


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


def clean_columns(data: pl.DataFrame) -> pl.DataFrame:
    """Normalize and filter DataFrame columns inside a pl.DataFrame.

    This function computes a mapping from normalized column names (via
    `preprocess_col`) to the original column names, applies the mapping to
    rename columns in place, and then drops any columns that are not listed
    in the module-level `DATA_COLUMNS`

    Args:
        data (pl.DataFrame): The DataFrame to be processed.

    Returns:
        pl.DataFrame: The processed DataFrame
    """
    columns = data.columns
    col_mappings = {preprocess_col(col): col for col in columns}
    data = data.rename(col_mappings)
    columns_to_drop = [col for col in columns if col not in DATA_COLUMNS]
    data = data.drop(columns_to_drop)
    return data
