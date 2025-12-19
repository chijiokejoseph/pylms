import pandas as pd

from ..cli import select_student
from ..constants import NAME
from ..data import DataStore
from ..errors import Result, Unit
from ..history import History, all_dates
from ..info import print_info
from ..paths_class import get_class_path
from ..record import RecordStatus
from .record_input import input_record


def edit_multiple_records(
    ds: DataStore, history: History, dates_to_mark: list[str]
) -> Result[Unit]:
    students_serials = select_student(ds)
    if students_serials.is_err():
        return students_serials.propagate()

    students_serials = students_serials.unwrap()

    pretty_names: pd.Series = ds.pretty()[NAME]
    data_ref: pd.DataFrame = ds.as_ref()
    for each_serial in students_serials:
        student_idx: int = each_serial - 1
        student_name: str = pretty_names.iloc[student_idx]
        for each_date in dates_to_mark:
            record_path = get_class_path(each_date, "record")
            if record_path.is_err():
                return record_path.propagate()

            record_path = record_path.unwrap()

            class_idx: int = all_dates(history, "").index(each_date)
            class_num: int = class_idx + 1
            if not record_path.exists():
                print_info(
                    f"There is no marked attendance for class {class_num} held on {each_date}. \nPlease mark the full attendance for that class before editing attendance manually for a subset of students for that same class."
                )
                continue
            print_info(
                f"You are editing Student {each_serial}: {student_name} attendance record for Class {class_num} held on {each_date}"
            )
            record_result = input_record(
                history,
                each_date,
                [RecordStatus.PRESENT, RecordStatus.ABSENT, RecordStatus.EXCUSED],
            )
            if record_result.is_err():
                return record_result.propagate()
            selected_record: RecordStatus = record_result.unwrap()
            data_ref.loc[student_idx, each_date] = selected_record

    return Result.unit()
