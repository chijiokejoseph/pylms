from pylms.utils import DataStore
from pylms.cli import input_record, select_student
from pylms.record import RecordStatus

import pandas as pd

def edit_batch_records(ds: DataStore, dates_to_mark: list[str]) -> DataStore:
    students_serials: list[int] = select_student(ds)
    idxs: list[int] = [serial - 1 for serial in students_serials]
    data: pd.DataFrame = ds()
    for each_date in dates_to_mark:
        selected_record = input_record(
            each_date,
            [RecordStatus.PRESENT, RecordStatus.ABSENT, RecordStatus.EXCUSED],
        )
        data.loc[idxs, each_date] = selected_record
    
    ds.data = data
    return ds
        