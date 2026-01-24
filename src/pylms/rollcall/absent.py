import polars as pl

from pylms.errors import Result, Unit

from ..constants import DATE
from ..data import DataStore, DataStream
from ..record import RecordStatus
from .names_filter import filter_names


def record_absent(ds: DataStore, turnout_stream: DataStream, turnout_date: str) -> Result[Unit]:
    """Record students as absent if they are not marked as present, excused, or CDS.
    
    Args:
        ds (DataStore): DataStore to update with attendance.
        turnout_stream (DataStream): Stream containing attendance data.
        turnout_date (str): Date of the class to record absences for.
    """
    data_ref = ds.as_ref()
    
    # If no turnout data, mark everyone as absent
    if turnout_stream.is_empty():
        data_ref = data_ref.with_columns(
            pl.lit(str(RecordStatus.ABSENT)).alias(turnout_date)
        )
        return ds.copy_from(data_ref)

    # Filter and process turnout data
    turnout = filter_names(turnout_stream)
    if turnout.is_err():
        return turnout.propagate()
    
    turnout_stream = turnout.unwrap()
    turnout_data = turnout_stream.as_ref()
    date_col: str = turnout_data[0, DATE]

    # Get current attendance records and update absent students
    class_record: list[str] = data_ref[date_col].to_list()
    new_class_record = [
        str(RecordStatus.ABSENT)
        if old_record
        not in [
            str(RecordStatus.PRESENT),
            str(RecordStatus.NO_CLASS),
            str(RecordStatus.EXCUSED),
            str(RecordStatus.CDS),
        ]
        else old_record
        for old_record in class_record
    ]

    # Update DataStore with new attendance records
    data_ref = data_ref.with_columns(
        pl.Series(date_col, new_class_record).alias(date_col)
    )
    return ds.copy_from(data_ref)
