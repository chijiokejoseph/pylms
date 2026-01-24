from ..data import DataStore, DataStream
from ..record import RecordStatus
from .record_fn import record


def record_excused(ds: DataStore, turnout_stream: DataStream) -> None:
    """Record students as excused in the DataStore.
    
    Args:
        ds (DataStore): DataStore to update with attendance.
        turnout_stream (DataStream): Stream containing excused students data.
    """
    return record(ds, turnout_stream, RecordStatus.EXCUSED)
