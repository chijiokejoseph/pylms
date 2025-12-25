import re

import pandas as pd

from ..data import DataStream


def clean_col_names(data_stream: DataStream[pd.DataFrame]) -> None:
    """Clean and normalize column names in a DataStream.

    This function formats the column names of the DataFrame contained in the
    provided `DataStream`. The following transformations are applied to each
    column name:

    - Strip leading and trailing whitespace and convert to title case.
    - Replace occurrences of "nysc" or "siwes" (case-insensitive) with their
      uppercase equivalents "NYSC" and "SIWES".
    - Rename columns in the DataFrame to the cleaned names while preserving
      column data.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame whose column names should be cleaned.

    Returns:
        None
    """
    data: pd.DataFrame = data_stream.as_ref()
    for old_column in data.columns:
        new_column: str = old_column.strip().title()

        regex_nysc: re.Pattern[str] = re.compile(r"nysc", flags=re.IGNORECASE)
        regex_siwes: re.Pattern[str] = re.compile(r"siwes", flags=re.IGNORECASE)

        matches_nysc: list[str] | None = re.findall(regex_nysc, new_column)
        matches_siwes: list[str] | None = re.findall(regex_siwes, new_column)

        if matches_nysc:  # if matches_nysc is truthy i.e., is not None
            for each_match in matches_nysc:
                new_column = new_column.replace(each_match, each_match.upper())

        if matches_siwes:  # if matches_siwes is truthy i.e., is not None
            for each_match in matches_siwes:
                new_column = new_column.replace(each_match, each_match.upper())

        data[new_column] = data[old_column]
        # drop the old column if the new column name `new_column` is different from the old column name `old_column`
        if new_column != old_column:
            data.drop(old_column, inplace=True)

    return
