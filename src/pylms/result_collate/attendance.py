import re
from pathlib import Path

import numpy as np
import pandas as pd

from ..constants import NAME, SERIAL
from ..data import DataStore, DataStream
from ..errors import LMSError, Result, Unit, eprint
from ..history import History, record_attendance, retrieve_dates
from ..info import printpass
from ..paths import get_paths_excel
from ..paths_class import get_class_path
from ..record import RecordStatus
from ..result_utils import (
    det_attendance_req_col,
    det_attendance_score_col,
    det_attendance_total_col,
    input_marks_req,
    list_print,
)


def _val_all_classes_recorded() -> Result[Unit]:
    dates_list = retrieve_dates("")
    if dates_list.is_err():
        return dates_list.propagate()

    dates_list = dates_list.unwrap()

    class_paths: list[Path] = []

    for each_date in dates_list:
        path = get_class_path(each_date, "class")
        if path.is_err():
            return path.propagate()
        path = path.unwrap()
        class_paths.append(path)

    record_paths: list[Path] = []
    for each_date in dates_list:
        path = get_class_path(each_date, "record")
        if path.is_err():
            return path.propagate()
        path = path.unwrap()
        record_paths.append(path)

    if len(class_paths) != len(record_paths):
        msg: str = f"The records of Classes with attendance generated have a length of {len(class_paths)} while the records of Classes with attendance marked have a length of {len(record_paths)}"
        eprint(msg)
        return Result.err(msg)

    def ret_exist_paths(paths_list: list[Path]) -> list[Path]:
        return [each_path for each_path in paths_list if each_path.exists()]

    exist_class_paths: list[Path] = ret_exist_paths(class_paths)
    valid_class_path_names: list[str] = [
        each_path.name for each_path in exist_class_paths
    ]
    exist_class_dir: Path = exist_class_paths[0].parent.resolve()
    exist_record_paths: list[Path] = ret_exist_paths(record_paths)
    valid_record_path_names: list[str] = [
        each_path.name for each_path in exist_record_paths
    ]
    exist_record_dir: Path = exist_record_paths[0].parent.resolve()
    for class_path, record_path in zip(exist_class_paths, exist_record_paths):

        def return_class_num(input_path: Path) -> int:
            filename: str = input_path.name
            matches: re.Match[str] | None = re.search(r"\d+\.json", filename)
            if matches is None:
                return 0
            matched_str: str = matches.group()
            class_num_str: str = matched_str.removesuffix(".json")
            class_num: int = int(class_num_str)
            return class_num

        if return_class_num(class_path) != return_class_num(record_path):
            msg = (
                "Not all existing records of Classes with attendance and existing records of Classes with attendance marked have a length that match. \n"
                + f"Existing Class Paths -> {list_print(valid_class_path_names)} at dir -> {exist_class_dir}\n"
                + f"Existing Record Paths -> {list_print(valid_record_path_names)} at dir -> {exist_record_dir}"
            )
            eprint(msg)
            return Result.err(msg)

    return Result.unit()


def _extract_class_held_dates(ds: DataStore) -> list[str]:
    data: pd.DataFrame = ds.as_ref()

    def test_col(col_data: pd.Series, col_name: str) -> bool:
        if re.fullmatch(r"^\d{2}/\d{2}/\d{4}$", col_name) is None:
            return False
        if any(
            [
                row_data
                in [
                    RecordStatus.NO_CLASS,
                    RecordStatus.EMPTY,
                    RecordStatus.EMPTY.strip(),
                ]
                for row_data in col_data.tolist()
            ]
        ):
            return False
        return True

    return [
        column for column in data.columns.tolist() if test_col(data[column], column)
    ]


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

    # Validate that all classes have been recorded
    check_result = _val_all_classes_recorded()
    if check_result.is_err():
        return check_result.propagate()

    # Extract the dates of classes that were held
    class_held_dates = _extract_class_held_dates(ds)

    # Retrieve and filter the relevant data for the held classes
    data: pd.DataFrame = ds.pretty()
    dates_data: pd.DataFrame = data.loc[:, class_held_dates]

    # Prompt the user to enter attendance requirement
    req_result = input_marks_req("Enter the Attendance Requirement [1 - 100]: ")
    if req_result.is_err():
        return Result.err(req_result.unwrap_err())
    req: int = req_result.unwrap()

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
        error = LMSError("Incomplete class records detected.")
        return Result.err(error)

    # Calculate attendance scores based on the number of classes held
    num_classes_held: int = len(class_held_dates)
    score_arr: np.ndarray = count_arr * 100 / num_classes_held
    score_arr = score_arr.round(2)

    # Determine column names for total, score, and requirement
    total_col: str = det_attendance_total_col(num_classes_held)
    score_col: str = det_attendance_score_col()
    req_col: str = det_attendance_req_col()

    # Create a DataFrame with collated attendance data
    collated_data: pd.DataFrame = pd.DataFrame(
        data={
            SERIAL: data[SERIAL].copy(),
            NAME: data[NAME].copy(),
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
