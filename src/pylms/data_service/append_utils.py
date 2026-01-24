import re

import polars as pl

from ..constants import NAME, SERIAL, SPACE_DELIM, UNIQUE_COLUMNS
from ..data import DataStore
from ..record import RecordStatus


def _clean_date(data: pl.DataFrame):
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


def clean_after_ops(ds: DataStore) -> None:
    """Clean DataStore after operations by updating serials and sorting.
    
    Args:
        ds (DataStore): DataStore to clean and update.
    """
    data_ref = ds.as_ref()
    # Update unique columns, sort by name, and reset serial numbers
    data_ref = data_ref.with_columns(
        pl.col(UNIQUE_COLUMNS).unique(),
        pl.col(NAME).sort(),
        pl.Series(SERIAL, [i + 1 for i in range(data_ref.shape[0])]).alias(SERIAL),
    )
    # Clean date columns
    data_ref = _clean_date(data_ref)
    _ = ds.copy_from(data_ref).unwrap()
