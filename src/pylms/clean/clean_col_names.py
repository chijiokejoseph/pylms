import re

import polars as pl

from pylms.constants import COMPLETION, DATA_COLUMNS

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

def clean_col_names(data: pl.DataFrame) -> pl.DataFrame:
    """Clean and normalize column names in a pl.DataFrame.

    This function formats the column names of the DataFrame contained in the
    provided `pl.DataFrame`. The following transformations are applied to each
    column name:

    - Strip leading and trailing whitespace and convert to title case.
    - Replace occurrences of "nysc" or "siwes" (case-insensitive) with their
      uppercase equivalents "NYSC" and "SIWES".
    - Rename columns in the DataFrame to the cleaned names while preserving
      column data.

    Args:
        data (DataFrame): The DataFrame whose column names should be cleaned.

    Returns:
        (DataFrame): The cleaned DataFrame
    """
    for old_column in data.columns:
        new_column: str = old_column.strip().title()

        regex_nysc: re.Pattern[str] = re.compile(r"nysc", flags=re.IGNORECASE)
        regex_siwes: re.Pattern[str] = re.compile(r"siwes", flags=re.IGNORECASE)

        matches_nysc: list[str] = re.findall(regex_nysc, new_column)
        matches_siwes: list[str] = re.findall(regex_siwes, new_column)

        if len(matches_nysc) > 0:  # if matches_nysc is truthy i.e., is not None
            for each_match in matches_nysc:
                new_column = new_column.replace(each_match, each_match.upper())

        if len(matches_siwes) > 0:  # if matches_siwes is truthy i.e., is not None
            for each_match in matches_siwes:
                new_column = new_column.replace(each_match, each_match.upper())

        data = data.rename({old_column: new_column})

    col_mappings = {preprocess_col(col): col for col in data.columns}
    data = data.rename(col_mappings)
    columns_to_drop = [col for col in data.columns if col not in DATA_COLUMNS]
    data = data.drop(columns_to_drop)
    data = data.with_columns(
        [pl.col(col) for col in DATA_COLUMNS if col not in data.columns]
    )

    return data
