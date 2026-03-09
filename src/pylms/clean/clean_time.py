import polars as pl

from ..constants import TIME, TIME_FMT


def clean_time(data: pl.DataFrame) -> pl.DataFrame:
    """Normalize the `TIME` column values in a pl.DataFrame's DataFrame.

    Applies the `_clean_time` helper to every entry in the column named by the
    `TIME` constant to produce a consistent, formatted time string for each
    row.

    Args:
        data (pl.DataFrame): The DataFrame whose `TIME` column should be normalized.

    Returns:
        pl.DataFrame: The processed DataFrame
    """
    return data.with_columns(pl.col(TIME).str.to_datetime().dt.strftime(TIME_FMT))
