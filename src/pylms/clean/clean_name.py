import polars as pl

from ..constants import NAME
from .rclean import clean_names


def clean_name(data: pl.DataFrame) -> pl.DataFrame:
    """Format the `NAME` column entries in a pl.DataFrame's DataFrame.

    Reads the DataFrame from `data`, applies the helper `_clean_name`
    to each value in the column identified by the `NAME` constant and mutates
    the DataFrame

    Args:
        data (pl.DataFrame): The DataFrame whose `NAME` column will be formatted.

    Returns:
        None
    """
    # name: np.ndarray = data[NAME].to_numpy()
    # name = _clean_name(name)
    # name = np.array(name, dtype=pl.String)
    # data = data.with_columns(
    #     pl.Series(NAME, data, dtype=pl.String)
    # )
    data = data.with_columns(pl.col(NAME).map_batches(clean_names))
    return data
