import polars as pl

from ..constants import EMAIL


def clean_email(data: pl.DataFrame) -> pl.DataFrame:
    """Normalize email addresses in the pl.DataFrame's DataFrame.

    Convert entries in the column named by `EMAIL` to lower case and strip
    surrounding whitespace. The operation is applied to the DataFrame obtained
    from `data`.

    Args:
        data (pl.DataFrame): The DataFrame with an email column to normalize.

    Returns:
        pl.DataFrame: The processed DataFrame
    """

    # email: np.ndarray = data[EMAIL].to_numpy()
    # email = apply(email)
    # email = np.array(email, dtype=np.str_)

    # data = data.with_columns(
    #     pl.Series(EMAIL, email, dtype=pl.String)
    # )

    data = data.with_columns(pl.col(EMAIL).str.to_lowercase().str.strip_chars())
    return data
