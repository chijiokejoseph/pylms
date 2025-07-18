from typing import cast

import pandas as pd

from pylms.cli import input_record
from pylms.record import RecordStatus
from pylms.rollcall import GlobalRecord
from pylms.utils import DataStore


def edit_all_records(ds: DataStore, dates_to_mark: list[str]) -> DataStore:
    for each_date in dates_to_mark:
        selected_record = input_record(
            each_date,
            [RecordStatus.PRESENT, RecordStatus.ABSENT, RecordStatus.NO_CLASS],
        )
        GlobalRecord().swap(each_date, selected_record)

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

        data: pd.DataFrame = ds()
        new_data: pd.DataFrame = data.copy()
        temp: list[str] = data[each_date].tolist()
        class_record = cast(list[RecordStatus], temp)
        new_class_record = [
            fill_record_fn(old_record, selected_record) for old_record in class_record
        ]
        new_data.loc[:, each_date] = new_class_record
        ds.data = new_data

    return ds
