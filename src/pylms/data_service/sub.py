from ..constants import SERIAL
from ..errors import Result, Unit
from ..data import DataStore
from .append_utils import clean_after_ops
import polars as pl


def sub(superset: DataStore, serial: list[int]) -> Result[Unit]:
    data_ref = superset.as_ref()
    data_ref = data_ref.remove(pl.col(SERIAL).is_in(serial))
    result = superset.copy_from(data_ref)
    if result.is_err():
        return result.propagate()

    clean_after_ops(superset)
    return Result.unit()
