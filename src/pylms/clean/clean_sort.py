import polars as pl

from ..constants import NAME, SERIAL


def clean_sort(data: pl.DataFrame) -> pl.DataFrame:
    """Sort rows by name and assign a 1-based serial number.

    Reads the DataFrame from `data`, sorts it in-place by the column
    identified by the `NAME` constant, assigns a 1-based sequence to the
    `SERIAL` column and resets the DataFrame index.

    Args:
        data (pl.DataFrame): The
            DataFrame to sort and number.

    Returns:
        None
    """
    return data.sort(pl.col(NAME)).with_columns(
        pl.Series(SERIAL, [i + 1 for i in range(data.shape[0])], pl.Int64).alias(SERIAL)
    )
