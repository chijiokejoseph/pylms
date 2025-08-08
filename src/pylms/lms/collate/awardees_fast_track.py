import pandas as pd

from pylms.cli import select_student
from pylms.cli.option_input import input_option
from pylms.data_ops import sub
from pylms.lms.collate.awardees import collate_awardees
from pylms.utils import DataStore, DataStream


def collate_fast_track(ds: DataStore) -> None:
    print("Enter the students to be fast tracked to the Advanced Class.")
    student_serials: list[int] = select_student(ds)
    menu: list[str] = ["Yes", "No"]
    i, _ = input_option(menu, prompt="Confirm the following students should be fast-tracked")
    if i != 1:
        print("\nFast Tracking has been cancelled.\n")
        return
    student_indices: list[int] = [serial - 1 for serial in student_serials]
    pretty_data: pd.DataFrame = ds.pretty()
    fast_track_data: pd.DataFrame = pretty_data.iloc[student_indices, :]
    collate_awardees(DataStream(fast_track_data), collate_type="fast track")
    print(
        "Students fast tracked to the Advanced Class have been collected. Removing them from DataStore."
    )
    sub(ds, student_serials)
    return
