from ..data import DataStore, DataStream
from ..errors import Result, Unit
from ..record import RecordStatus
from .record_fn import record


def record_present(ds: DataStore, turnout_stream: DataStream) -> Result[Unit]:
    """Record students as present in the DataStore.

    Args:
        ds (DataStore): DataStore to update with attendance.
        turnout_stream (DataStream): Stream containing present students data.
    """
    return record(ds, turnout_stream, RecordStatus.PRESENT)
