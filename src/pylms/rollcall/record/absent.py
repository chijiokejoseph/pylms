import pandas as pd

from pylms.constants import DATE
from pylms.record import RecordStatus
from pylms.rollcall.record.names_filter import filter_names
from pylms.utils import DataStore, DataStream


def record_absent(ds: DataStore, turnout_stream: DataStream[pd.DataFrame], turnout_date: str) -> DataStore:
    if turnout_stream.is_empty():
        data: pd.DataFrame = ds()
        data[turnout_date] = RecordStatus.ABSENT
        ds.data = data
        return ds
        
    turnout_stream = filter_names(turnout_stream)
    turnout_data: pd.DataFrame = turnout_stream()
    date_col: str = turnout_data[DATE].iloc[0]

    data = ds()
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

    data[date_col] = new_class_record
    ds.data = data
    return ds
