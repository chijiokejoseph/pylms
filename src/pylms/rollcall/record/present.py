import pandas as pd

from pylms.record import RecordStatus
from pylms.rollcall.record.record_fn import record
from pylms.utils import DataStore, DataStream


def record_present(
    ds: DataStore, turnout_stream: DataStream[pd.DataFrame]
) -> DataStore:
    return record(ds, turnout_stream, RecordStatus.PRESENT)
