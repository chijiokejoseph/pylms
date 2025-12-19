import pandas as pd

from ..data import DataStore, DataStream
from ..record import RecordStatus
from .record_fn import record


def record_excused(ds: DataStore, turnout_stream: DataStream[pd.DataFrame]) -> None:
    return record(ds, turnout_stream, RecordStatus.EXCUSED)
