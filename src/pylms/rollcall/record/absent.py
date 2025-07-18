import pandas as pd

from pylms.constants import DATE
from pylms.record import RecordStatus
from pylms.rollcall.record.names_filter import filter_names
from pylms.utils import DataStore, DataStream


def record_absent(ds: DataStore, turnout_stream: DataStream[pd.DataFrame]) -> DataStore:
    turnout_stream = filter_names(turnout_stream)
    turnout_data: pd.DataFrame = turnout_stream()
    date_col: str = turnout_data[DATE].iloc[0]

    data: pd.DataFrame = ds()
    new_data: pd.DataFrame = data.copy()
    class_record: list[str] = data[date_col].tolist()
    new_class_record: list[str] = [
        RecordStatus.ABSENT
        if old_record
        not in [
            RecordStatus.PRESENT,
            RecordStatus.NO_CLASS,
            RecordStatus.EXCUSED,
            RecordStatus.CDS,
        ]
        else old_record
        for old_record in class_record
    ]

    new_data[date_col] = new_class_record
    ds.data = new_data
    return ds
