from pylms.utils import DataStore
from pylms.cli import input_record, select_student
from pylms.record import RecordStatus

import pandas as pd

def edit_batch_records(ds: DataStore, dates_to_mark: list[str]) -> None:
    students_serials: list[int] = select_student(ds)
    idxs: list[int] = [serial - 1 for serial in students_serials]
    data_ref: pd.DataFrame = ds.as_ref()
    for each_date in dates_to_mark:
        record_result = input_record(
            each_date,
            [RecordStatus.PRESENT, RecordStatus.ABSENT, RecordStatus.EXCUSED],
        )
        if record_result.is_err():
            return
        selected_record: RecordStatus = record_result.unwrap()
        data_ref.loc[idxs, each_date] = selected_record
        
    return None
        