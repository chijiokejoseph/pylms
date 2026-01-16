from pathlib import Path

import numpy as np
import pandas as pd

from ..constants import COMMA_DELIM, NAME, SERIAL
from ..data import DataStore, DataStream
from ..errors import Result, Unit, eprint
from ..history import (
    History,
    get_held_classes,
    get_unrecorded_classes,
    record_attendance,
)
from ..info import printpass
from ..paths import get_paths_excel
from ..record import RecordStatus
from ..result_utils import (
    det_attendance_req_col,
    det_attendance_score_col,
    det_attendance_total_col,
    input_marks_req,
)


def collate_attendance(ds: DataStore, history: History) -> Result[Unit]:
    """
    Collate the attendance spreadsheet for the students.

    The attendance spreadsheet should have all the Classes held marked.

    The collated data will be saved in the Attendance.xlsx file in the Data folder.

    :param ds: (DataStore) - The data to be collated
    :type ds: DataStore
    :param history: (History) - The state of the application
    :type history: History

    :return: (Result[Unit]) - returns a unit result
    :rtype: Result[Unit]
    """

    # Extract the dates of classes that were held
    held_dates = get_held_classes(history, "")
    unrecorded_dates = get_unrecorded_classes(history, "")

    if len(unrecorded_dates) > 0:
        dates_print = COMMA_DELIM.join(unrecorded_dates)
        msg = f"Dates: {dates_print} have been held but have not been marked yet. Please mark before collating attendance"
        eprint(msg)
        return Result.err(msg)

    # Retrieve and filter the relevant data for the held classes
    pretty = ds.to_pretty()
    data = ds.as_ref()
    dates_data: pd.DataFrame = data.loc[:, held_dates]

    # Prompt the user to enter attendance requirement
    req = input_marks_req("Enter the Attendance Requirement [1 - 100]: ")

    if req.is_err():
        return req.propagate()

    req = req.unwrap()

    # Define a function to map attendance status to integer values
    def map_to_int(value: str) -> int:
        match True:
            case _ if value == RecordStatus.ABSENT:
                return 0
            case _:
                return 1

    # Map attendance data to integers and calculate the total count per student
    count_data: pd.DataFrame = dates_data.map(map_to_int)  # pyright: ignore[reportUnknownMemberType]
    count_arr: np.ndarray = count_data.to_numpy()
    count_arr = count_arr.sum(axis=1)
    count_arr = count_arr.flatten()

    # Check if all attendance records are complete
    max_len: int = max(count_arr.shape)
    if max_len != count_data.shape[0]:
        msg = "Incomplete class records detected."
        eprint(msg)
        return Result.err(msg)

    # Calculate attendance scores based on the number of classes held
    num_classes_held: int = len(held_dates)
    score_arr: np.ndarray = count_arr * 100 / num_classes_held
    score_arr = score_arr.round(2)

    # Determine column names for total, score, and requirement
    total_col: str = det_attendance_total_col(num_classes_held)
    score_col: str = det_attendance_score_col()
    req_col: str = det_attendance_req_col()

    # Create a DataFrame with collated attendance data
    collated_data: pd.DataFrame = pd.DataFrame(
        data={
            SERIAL: data[SERIAL],
            NAME: pretty[NAME],
            total_col: count_arr.astype(np.int64).round(0),
            score_col: score_arr.astype(np.float64).round(2),
            req_col: req,
        }
    )

    # Notify user that attendance has been recorded successfully
    printpass("Attendance recorded successfully\n")

    # Save the collated data to an Excel file
    path: Path = get_paths_excel()["Attendance"]

    result = DataStream(collated_data).to_excel(path)
    if result.is_err():
        return result.propagate()

    # Record attendance in the history
    record_attendance(history)

    return Result.unit()
