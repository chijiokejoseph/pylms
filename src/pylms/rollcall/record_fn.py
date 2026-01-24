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
    data_ref = ds.as_ref()
    
    turnout = filter_names(turnout_stream)
    if turnout.is_err():
        return turnout.propagate()
    
    turnout_stream = turnout.unwrap()
    turnout_data = turnout_stream.as_ref()
    
    # Get student names and class date
    present_names: list[str] = turnout_data[NAME].to_list()
    class_date = turnout_data[0, DATE]
    
    # Get all student names from DataStore
    all_names: list[str] = data_ref[NAME].to_list()
    
    # Get current attendance records for the class date
    class_record: list[str] = data_ref[class_date].to_list()
    
    # Update records for students in turnout data
    new_class_record = [
        str(fill_value) if each_name in present_names else old_record
        for each_name, old_record in zip(all_names, class_record)
    ]
    
    # Update DataStore with new records
    data_ref = data_ref.with_columns(
        pl.Series(class_date, new_class_record).alias(class_date)
    )
    return ds.copy_from(data_ref)
