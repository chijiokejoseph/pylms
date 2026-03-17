import re

import polars as pl

from ..constants import SPACE_DELIM
from ..record import RecordStatus


def clean_attendance(data: pl.DataFrame) -> pl.DataFrame:
    """Clean date columns by standardizing attendance status values.

    Args:
        data (pl.DataFrame): DataFrame with date columns to clean.

    Returns:
        pl.DataFrame: DataFrame with cleaned date columns.
    """
    reg = re.compile(r"^\d{2}/\d{2}/\d{4}$")
    data = data.with_columns(
        [
            pl.when(pl.col(column).unique().is_in([str(RecordStatus.NO_CLASS)]))
            .then(pl.lit(str(RecordStatus.NO_CLASS)).alias(column))
            .otherwise(
                pl.when(pl.col(column).is_in([str(RecordStatus.PRESENT)])).then(
                    pl.when(pl.col(column) == SPACE_DELIM)
                    .then(pl.lit(RecordStatus.PRESENT))
                    .otherwise(pl.col(column))
                )
            )
            for column in data.columns
            if reg.fullmatch(column) is not None
        ]
    )
    return data
