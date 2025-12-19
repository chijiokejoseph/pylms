import pandas as pd

from ..cli import select_student
from ..data import DataStore
from ..errors import Result, Unit
from ..history import History
from ..record import RecordStatus
from .record_input import input_record


def edit_batch_records(
    ds: DataStore, history: History, dates_to_mark: list[str]
) -> Result[Unit]:
    students_serials = select_student(ds)
    if students_serials.is_err():
        return students_serials.propagate()

    students_serials = students_serials.unwrap()

    idxs: list[int] = [serial - 1 for serial in students_serials]
    data_ref: pd.DataFrame = ds.as_ref()
    for each_date in dates_to_mark:
        record_result = input_record(
            history,
            each_date,
            [RecordStatus.PRESENT, RecordStatus.ABSENT, RecordStatus.EXCUSED],
        )
        if record_result.is_err():
            return record_result.propagate()

        selected_record: RecordStatus = record_result.unwrap()
        data_ref.loc[idxs, each_date] = selected_record

    return Result.unit()
