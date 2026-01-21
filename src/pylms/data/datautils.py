from typing import overload

import numpy as np
from numpy.typing import DTypeLike
import polars as pl


@overload
def datamap(
    data: pl.DataFrame,
    col: str,
    func: np.vectorize,
    np_type: DTypeLike,
    pl_type: pl.DataType,
    new_col: str | None = None,
) -> pl.DataFrame:
    pass


@overload
def datamap(
    data: pl.Series,
    col: str,
    func: np.vectorize,
    np_type: DTypeLike,
    pl_type: pl.DataType,
    new_col: str | None = None,
) -> pl.Series:
    pass


def datamap(
    data: pl.DataFrame | pl.Series,
    col: str,
    func: np.vectorize,
    np_type: DTypeLike,
    pl_type: pl.DataType,
    new_col: str | None = None
) -> pl.Series | pl.DataFrame | pl.LazyFrame:
    if isinstance(data, pl.DataFrame):
        series = data[col].to_numpy()
    else:
        series = data.to_numpy()
    series = func(series)
    series = np.array(series, dtype=np_type)
    if isinstance(data, pl.Series):
        return pl.Series(col, series, pl_type)

    if new_col is None:
        new_col = col

    return data.with_columns(pl.Series(new_col, series, dtype=pl_type).alias(new_col))


def map_(
    data: pl.Series,
    func: np.vectorize,
    np_type: np.dtype,
    pl_type: pl.DataType,
    col: str,
):
    series = data.to_numpy()
    series = func(series)
    series = np.array(series, dtype=np_type)
    return pl.Series(col, series, pl_type)
