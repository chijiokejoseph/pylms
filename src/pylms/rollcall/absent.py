import polars as pl

from ..data import DataStore
from ..errors import Result, Unit
from ..record import RecordStatus

VALID_RECORDS = [
    str(RecordStatus.PRESENT),
    str(RecordStatus.NO_CLASS),
    str(RecordStatus.EXCUSED),
    str(RecordStatus.CDS),
]


def record_absent(ds: DataStore, turnout_date: str) -> Result[Unit]:
    """Record students as absent if they are not marked as present, excused, or CDS.

    Args:
        ds (DataStore): DataStore to update with attendance.
        turnout_stream (DataStream): Stream containing attendance data.        turnout_date (str): Date of the class to record absences for.
    """
    data_ref = ds.as_ref()

    data_ref = data_ref.with_columns(
        pl.when(~pl.col(turnout_date).is_in(VALID_RECORDS))
        .then(pl.lit(str(RecordStatus.ABSENT)))
        .otherwise(pl.col(turnout_date))
        .alias(turnout_date)
    )
    return ds.copy_from(data_ref)
