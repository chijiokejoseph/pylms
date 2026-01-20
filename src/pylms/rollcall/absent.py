from ..constants import DATE
from ..data import DataStore, DataStream
from ..record import RecordStatus
from .names_filter import filter_names


def record_absent(ds: DataStore, turnout_stream: DataStream, turnout_date: str) -> None:
    data_ref: pl.DataFrame = ds.as_ref()
    if turnout_stream.is_empty():
        data_ref[turnout_date] = RecordStatus.ABSENT
        return None

    turnout_stream = filter_names(turnout_stream)
    turnout_data: pl.DataFrame = turnout_stream()
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
    return None
