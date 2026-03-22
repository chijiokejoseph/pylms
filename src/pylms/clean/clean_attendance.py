import re

import polars as pl

from ..constants import SPACE_DELIM
from ..record import RecordStatus


def check_for_edit_all(col: str, record: RecordStatus) -> pl.Expr:
    positive_case = pl.col(col) == str(record)
    otherwise = pl.col(col) == str(RecordStatus.CDS)
    return (positive_case | otherwise).any()


def clean_attendance(data: pl.DataFrame) -> pl.DataFrame:
    """Clean date columns by standardizing attendance status values.

    Args:
        data (pl.DataFrame): DataFrame with date columns to clean.

    Returns:
        pl.DataFrame: DataFrame with cleaned date columns.
    """
    reg = re.compile(r"^\d{2}/\d{2}/\d{4}$")
    date_cols = [col for col in data.columns if reg.fullmatch(col) is not None]
    for column in date_cols:
        data = data.with_columns(
            pl.when(check_for_edit_all(column, RecordStatus.NO_CLASS))
            .then(pl.lit(str(RecordStatus.NO_CLASS)).alias(column))
            .otherwise(
                pl.when(check_for_edit_all(column, RecordStatus.PRESENT))
                .then(
                    pl.when(pl.col(column) == SPACE_DELIM)
                    .then(pl.lit(RecordStatus.PRESENT))
                    .otherwise(
                        pl.when(pl.col(column) == SPACE_DELIM)
                        .then(pl.lit(str(RecordStatus.ABSENT)))
                        .otherwise(pl.col(column))
                    )
                )
                .otherwise(pl.col(column))
            )
            .alias(column)
        )
    return data
