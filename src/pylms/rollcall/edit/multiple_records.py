from pathlib import Path

import pandas as pd

from pylms.cli import input_record, select_student
from pylms.constants import NAME
from pylms.record import RecordStatus
from pylms.utils import DataStore, date, paths


def edit_multiple_records(ds: DataStore, dates_to_mark: list[str]) -> DataStore:
    student_serials: list[int] = select_student(ds)
    pretty_names: pd.Series = ds.pretty()[NAME]
    data_ref: pd.DataFrame = ds.as_ref()
    for each_serial in student_serials:
        student_idx: int = each_serial - 1
        student_name: str = pretty_names.iloc[student_idx]
        for each_date in dates_to_mark:
            record_path: Path = paths.get_class_path(each_date, "record")
            class_idx: int = date.retrieve_dates().index(each_date)
            class_num: int = class_idx + 1
            if not record_path.exists():
                print(
                    f"There is no marked attendance for class {class_num} held on {each_date}. \nPlease mark the full attendance for that class before editing attendance manually for a subset of students for that same class."
                )
                continue
            print(
                f"You are editing Student {each_serial}: {student_name} attendance record for Class {class_num} held on {each_date}"
            )
            selected_record: RecordStatus = input_record(
                each_date,
                [RecordStatus.PRESENT, RecordStatus.ABSENT, RecordStatus.EXCUSED],
            )
            data_ref.loc[student_idx, each_date] = selected_record

    return ds
