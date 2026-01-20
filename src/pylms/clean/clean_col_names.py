import re

import polars as pl


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
            data = data.drop(old_column)

    return data
