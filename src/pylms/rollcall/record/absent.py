import pandas as pd

from pylms.constants import DATE
from pylms.record import RecordStatus
from pylms.rollcall.record.names_filter import filter_names
from pylms.utils import DataStore, DataStream


def record_absent(ds: DataStore, turnout_stream: DataStream[pd.DataFrame], turnout_date: str) -> DataStore:
    data_ref: pd.DataFrame = ds.as_ref()
    if turnout_stream.is_empty():
        data_ref[turnout_date] = RecordStatus.ABSENT
        return ds
        
    turnout_stream = filter_names(turnout_stream)
    turnout_data: pd.DataFrame = turnout_stream()
    date_col: str = turnout_data[DATE].iloc[0]

    class_record: list[str] = data_ref[date_col].tolist()
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

    data_ref[date_col] = new_class_record
    return ds
