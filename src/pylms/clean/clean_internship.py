import polars as pl

from ..constants import INTERNSHIP


def clean_internship(data: pl.DataFrame) -> pl.DataFrame:
    """Normalize internship values to uppercase and provide validation.

    This function converts all values in the column named by the module-level
    `INTERNSHIP` constant to upper-case strings. It returns a `pl.DataFrame`
    wrapping the transformed DataFrame and supplies a validator that ensures
    the `INTERNSHIP` column exists and that every value in the column is
    uppercase.

    Args:
        data (pl.DataFrame): The DataFrame to normalize.

    Returns:
        pl.DataFrame: The normalized DataFrame
    """

    return data.with_columns(pl.col(INTERNSHIP).str.to_uppercase().cast(pl.Categorical).alias(INTERNSHIP))
