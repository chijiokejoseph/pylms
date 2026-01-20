import polars as pl

from ..constants import NA_COLUMNS_FILL, TRAINING


def clean_training(data: pl.DataFrame) -> pl.DataFrame:
    """Fill the `TRAINING` column with the configured default value.

    This function obtains the DataFrame from the provided `pl.DataFrame`, looks
    up the default fill value for the `TRAINING` column from the
    `NA_COLUMNS_FILL` mapping, assigns that value to the entire `TRAINING`
    column, and returns the modified DataFrame wrapped in a `pl.DataFrame`.

    Args:
        data (pl.DataFrame): The
            DataFrame whose `TRAINING` column should be filled.

    Returns:
        pl.DataFrame: A pl.DataFrame wrapping the DataFrame with the
            `TRAINING` column set to the default fill value.
    """
    training = NA_COLUMNS_FILL[TRAINING]

    if isinstance(training, str):
        data = data.with_columns(pl.lit(training).alias(TRAINING))

    return data
