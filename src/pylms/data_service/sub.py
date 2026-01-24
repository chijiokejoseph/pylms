from ..constants import SERIAL
from ..errors import Result, Unit
from ..data import DataStore
from .append_utils import clean_after_ops
import polars as pl


def sub(superset: DataStore, serial: list[int]) -> Result[Unit]:
    """Remove students with specified serial numbers from DataStore.
    
    Args:
        superset (DataStore): DataStore to remove students from.
        serial (list[int]): List of serial numbers to remove.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    data_ref = superset.as_ref()
    # Filter out rows with serial numbers in the removal list
    data_ref = data_ref.filter(~pl.col(SERIAL).is_in(serial))
    result = superset.copy_from(data_ref)
    if result.is_err():
        return result.propagate()

    # Clean up after removal operation
    clean_after_ops(superset)
    return Result.unit()
