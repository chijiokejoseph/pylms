import polars as pl

from ..constants import UNIQUE_COLUMNS


def clean_duplicates_with_cols(
    data: pl.DataFrame, identifier_columns: list[str]
) -> pl.DataFrame:
    """Remove duplicate rows from a pl.DataFrame using specified columns.

    This function removes duplicate rows from the DataFrame contained in the
    provided `pl.DataFrame` by using the supplied `identifier_columns` to
    determine row uniqueness. The resulting DataFrame has its index reset and
    is returned wrapped in a `pl.DataFrame`.

    Args:
        data (pl.DataFrame): The DataFrame to deduplicate.
        identifier_columns (list[str]): Column names used to identify duplicate
            rows.

    Returns:
        pl.DataFrame: A deduplicated DataFrame
    """
    return data.unique(subset=identifier_columns)


def clean_duplicates(data: pl.DataFrame) -> pl.DataFrame:
    """Remove duplicate rows from a pl.DataFrame using the default schema.

    Removes duplicate rows from the DataFrame contained in `data`
    using the module-level `UNIQUE_COLUMNS` list to determine uniqueness.
    The index of the deduplicated DataFrame is reset.

    Args:
        data (pl.DataFrame): The
            DataFrame to deduplicate.

    Returns:
        pl.DataFrame: A deduplicated DataFrame
    """
    return data.unique(UNIQUE_COLUMNS)
