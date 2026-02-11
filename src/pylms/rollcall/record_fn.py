import pandas as pd

from ..constants import DATE, NAME
from ..data import DataStore, DataStream
from ..record import RecordStatus, retrieve_record
from .names_filter import filter_names


def fill(old_value: str, new_value: RecordStatus) -> RecordStatus:
    old_record = retrieve_record(old_value)

    match old_record:
        # If old record is not the best (empty or absent) return new value
        case RecordStatus.EMPTY | RecordStatus.ABSENT:
            return new_value
        # If old record is (CDS, NO_CLASS or PRESENT) which are immutable or good, retain
        case RecordStatus.CDS | RecordStatus.NO_CLASS | RecordStatus.PRESENT:
            return old_record
        # If old record is excused and new is present, return present
        case _ if (
            old_record == RecordStatus.EXCUSED and new_value == RecordStatus.PRESENT
        ):
            return new_value
        # If old record is excused and new is absent, return excused
        case _ if (
            old_record == RecordStatus.EXCUSED and new_value == RecordStatus.ABSENT
        ):
            return old_record
        # Else return new record unequivocally
        case _:
            return new_value


def record(
    ds: DataStore, turnout_stream: DataStream[pd.DataFrame], fill_value: RecordStatus
) -> None:
    pretty = ds.to_pretty()
    data_ref = ds.as_ref()
    all_names = pretty.loc[:, NAME].astype(str)

    turnout_stream = filter_names(turnout_stream)
    turnout_data = turnout_stream()
    present_names = turnout_data.loc[:, NAME].astype(str)
    class_date: str = turnout_data[DATE].iloc[0]

    class_record = data_ref.loc[:, class_date].astype(str)

    new_class_record = [
        str(fill(old_record, fill_value))
        if each_name in present_names.tolist()
        else old_record
        for each_name, old_record in zip(all_names, class_record)
    ]
    data_ref.loc[:, class_date] = new_class_record
    return None
