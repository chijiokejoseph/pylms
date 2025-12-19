import pandas as pd

from pylms.errors import Result, Unit

from ..cli import input_option, select_student
from ..data import DataStore, DataStream
from ..data_service import sub
from ..info import print_info
from .awardees import collate_awardees


def collate_fast_track(ds: DataStore) -> Result[Unit]:
    print("Enter the students to be fast tracked to the Advanced Class.")
    student_serials = select_student(ds)
    if student_serials.is_err():
        return student_serials.propagate()

    student_serials = student_serials.unwrap()

    menu: list[str] = ["Yes", "No"]
    result = input_option(
        menu, prompt="Confirm the following students should be fast-tracked"
    )
    if result.is_err():
        return result.propagate()
    i, _ = result.unwrap()
    if i != 1:
        print_info("\nFast Tracking has been cancelled.\n")
        return Result.unit()

    student_indices: list[int] = [serial - 1 for serial in student_serials]
    pretty_data: pd.DataFrame = ds.pretty()
    fast_track_data: pd.DataFrame = pretty_data.iloc[student_indices, :]

    result = collate_awardees(DataStream(fast_track_data), collate_type="fast track")
    if result.is_err():
        return result.propagate()

    print_info(
        "Students fast tracked to the Advanced Class have been collected. Removing them from DataStore."
    )
    sub(ds, student_serials)
    return Result.unit()
