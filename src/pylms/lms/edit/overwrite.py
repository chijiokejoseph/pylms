from pathlib import Path
from typing import Callable, cast

import numpy as np
import pandas as pd

from pylms.cli import input_option, input_str, select_student
from pylms.constants import ValidateDataFn
from pylms.errors import LMSError, Result, Unit
from pylms.lms.collate.recollate import recollate
from pylms.lms.utils import (
    det_assessment_req_col,
    det_attendance_req_col,
    det_passmark_col,
    find_col,
    val_result_data,
)
from pylms.utils import DataStore, DataStream, paths, print_stream, read_data


def _parse(
    value: str,
    col: str,
    test_fn: Callable[[float], bool] = lambda x: 0 <= x <= 100,
    parse_fail_msg: str | None = None,
    test_fail_msg: str | None = None,
) -> float | None:
    if parse_fail_msg is None:
        parse_fail_msg = (
            f"The input to column {col} should be a positive number between 1 and 100"
        )
    if test_fail_msg is None:
        test_fail_msg = f"The input to column {col} should be between 0 and 100."

    try:
        if test_fn(float(value)):
            return float(value)
        print(test_fail_msg)
        return None
    except ValueError:
        print(
            parse_fail_msg,
        )
        return None


def get_mutable_cols(data_stream: DataStream[pd.DataFrame]) -> list[str]:
    return [
        find_col(data_stream, "Attendance", "Req").unwrap(),
        find_col(data_stream, "Assessment", "Req").unwrap(),
        find_col(data_stream, "Result", "Req").unwrap(),
        find_col(data_stream, "Assessment", "Score").unwrap(),
        find_col(data_stream, "Project", "Score").unwrap(),
        find_col(data_stream, "Result", "Score").unwrap(),
    ]


def _preprocess(
    data_stream: DataStream[pd.DataFrame], col: str, value: str
) -> float | None:
    match str(col):
        case _ if col in [
            find_col(data_stream, "Attendance", "Score").unwrap(),
            find_col(data_stream, "Attendance", "Count").unwrap(),
        ]:
            return None
        case _ if col in get_mutable_cols(data_stream):
            return _parse(value, col)
        case _:
            return None


def overwrite_result(ds: DataStore) -> Result[Unit]:
    result_path: Path = paths.get_paths_excel()["Result"]
    if not result_path.exists():
        return Result[Unit].err(
            LMSError(
                "Results has not been generated yet. Please collate results before running this operation"
            )
        )

    result_data: pd.DataFrame = read_data(result_path)
    result_stream: DataStream[pd.DataFrame] = DataStream(
        result_data, cast(ValidateDataFn, val_result_data)
    )
    result_data = result_stream()
    serials: list[int] = select_student(ds)
    for serial in serials:
        idx = serial - 1
        print_stream(result_stream, [serial])
        mutable_cols: list[str] = get_mutable_cols(result_stream)
        proc_value: float | None = None
        column: str = ""
        while proc_value is None:
            option_result = input_option(mutable_cols, "Result Cols to Edit")
            if option_result.is_err():
                option_result.print_if_err()
                return Result[Unit].err(option_result.unwrap_err())
            _, column = option_result.unwrap()
            value_result = input_str(
                f"Enter the new value for {column}: ", lower_case=False
            )
            if value_result.is_err():
                value_result.print_if_err()
                return Result[Unit].err(value_result.unwrap_err())
            proc_value = _preprocess(result_stream, column, value_result.unwrap())
            print()

        type_value = result_data.loc[:, column].dtype
        column_type = cast(np.dtype, type_value)
        new_value = np.array(proc_value).astype(column_type)
        match True:
            case _ if column in [
                det_attendance_req_col(),
                det_assessment_req_col(),
                det_passmark_col(),
            ]:
                result_data.loc[:, column] = new_value
            case _ if column in [
                find_col(result_stream, "Assessment", "Score").unwrap(),
                find_col(result_stream, "Project", "Score").unwrap(),
                find_col(result_stream, "Result", "Score").unwrap(),
            ]:
                result_data.loc[idx, column] = new_value
            case _:
                pass
        print()
    recollate(DataStream(result_data)).to_excel(result_path)
    return Result[Unit].unit()
