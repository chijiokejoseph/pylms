from typing import cast

import pandas as pd

from ..data import DataStore
from ..errors import Result, Unit
from ..history import History
from ..record import RecordStatus
from ..rollcall import GlobalRecord
from .record_input import input_record


def edit_all_records(
    ds: DataStore, history: History, dates_to_mark: list[str]
) -> Result[Unit]:
    for each_date in dates_to_mark:
        record_result = input_record(
            history,
            each_date,
            [RecordStatus.PRESENT, RecordStatus.ABSENT, RecordStatus.NO_CLASS],
        )
        if record_result.is_err():
            return record_result.propagate()
        selected_record: RecordStatus = record_result.unwrap()

        global_record = GlobalRecord.new()
        if global_record.is_err():
            return global_record.propagate()

        global_record = global_record.unwrap()
        global_record.swap(each_date, selected_record)

        def fill_record_fn(
            existing_record: RecordStatus, fill_record: RecordStatus
        ) -> RecordStatus:
            # If no class is held that day return no class
            if fill_record == RecordStatus.NO_CLASS:
                return fill_record

            # If the student's record indicates that that day is his CDS, then prefer the CDS record
            if existing_record == RecordStatus.CDS:
                return existing_record

            # If all the students are marked absent but a student is marked excused, prefer his excused record
            if (
                fill_record == RecordStatus.ABSENT
                and existing_record == RecordStatus.EXCUSED
            ):
                return existing_record

            # Else unequivocally return the fill record set by the user.
            return fill_record

        data_ref: pd.DataFrame = ds.as_ref()
        temp: list[str] = data_ref[each_date].tolist()
        class_record = cast(list[RecordStatus], temp)
        new_class_record = [
            fill_record_fn(old_record, selected_record) for old_record in class_record
        ]
        data_ref.loc[:, each_date] = new_class_record

    return Result.unit()
