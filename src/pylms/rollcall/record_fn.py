import polars as pl

from ..constants import DATE, NAME
from ..data import DataStore, DataStream
from ..record import RecordStatus
from .names_filter import filter_names
from ..errors import Result, Unit


def record(ds: DataStore, turnout_stream: DataStream, fill_value: RecordStatus) -> Result[Unit]:
    """Record attendance status for students in turnout data.
    
    Args:
        ds (DataStore): DataStore to update with attendance records.
        turnout_stream (DataStream): Stream containing student attendance data.
        fill_value (RecordStatus): Status to assign to students in turnout data.
    """
    data_ref = ds.pretty()
    
    turnout = filter_names(turnout_stream)
    if turnout.is_err():
        return turnout.propagate()
    
    turnout_stream = turnout.unwrap()
    turnout_data = turnout_stream.as_ref()
    
    # Get student names and class date
    present_names: list[str] = turnout_data[NAME].to_list()
    class_date: str = turnout_data[0, DATE]

    # Mark students with `fill_value`
    data_ref = data_ref.with_columns(
        pl.when(pl.col(NAME).is_in(present_names))
        .then(pl.lit(str(fill_value)))
        .otherwise(pl.col(class_date))
        .alias(class_date)
    )
    
    # Update DataStore with new records
    return ds.copy_from(data_ref)
