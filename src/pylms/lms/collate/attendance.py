import re
from pathlib import Path

import numpy as np
import pandas as pd

from pylms.constants import NAME, SERIAL
from pylms.lms.collate.errors import CollateIncompleteErr
from pylms.lms.utils import (
    det_attendance_req_col,
    det_attendance_score_col,
    det_attendance_total_col,
    list_print,
)
from pylms.record import RecordStatus
from pylms.utils import DataStore, DataStream, date, paths


def _val_all_classes_recorded() -> None:
    dates_list: list[str] = date.retrieve_dates()
    class_paths: list[Path] = [
        paths.get_class_path(each_date, "class") for each_date in dates_list
    ]
    record_paths: list[Path] = [
        paths.get_class_path(each_date, "record") for each_date in dates_list
    ]

    if len(class_paths) != len(record_paths):
        msg: str = f"The records of Classes with attendance generated have a length of {len(class_paths)} while the records of Classes with attendance marked have a length of {len(record_paths)}"
        raise CollateIncompleteErr(msg)

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
            raise CollateIncompleteErr(msg)

    return None


def _extract_class_held_dates(ds: DataStore) -> list[str]:
    data: pd.DataFrame = ds()

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


def collate_attendance(ds: DataStore, req: float) -> DataStream[pd.DataFrame]:
    _val_all_classes_recorded()
    class_held_dates = _extract_class_held_dates(ds)
    data: pd.DataFrame = ds.pretty()
    dates_data: pd.DataFrame = data.loc[:, class_held_dates]

    def map_to_int(value: str) -> int:
        match True:
            case _ if value == RecordStatus.ABSENT:
                return 0
            case _:
                return 1

    count_data: pd.DataFrame = dates_data.map(map_to_int)
    count_arr: np.ndarray = count_data.to_numpy()
    count_arr = count_arr.sum(axis=1)
    count_arr = count_arr.flatten()
    max_len: int = max(count_arr.shape)
    if max_len != count_data.shape[0]:
        raise CollateIncompleteErr("Just did it for doing sake")
    num_classes_held: int = len(class_held_dates)
    score_arr: np.ndarray = count_arr * 100 / num_classes_held
    score_arr = score_arr.round(2)

    total_col: str = det_attendance_total_col(num_classes_held)
    score_col: str = det_attendance_score_col()
    req_col: str = det_attendance_req_col()
    collated_data: pd.DataFrame = pd.DataFrame(
        data={
            SERIAL: data[SERIAL].copy(),
            NAME: data[NAME].copy(),
            total_col: count_arr.astype(np.int64).round(0),
            score_col: score_arr.astype(np.float64).round(2),
            req_col: req,
        }
    )
    print("\nAttendance recorded successfully\n")
    return DataStream(collated_data)
