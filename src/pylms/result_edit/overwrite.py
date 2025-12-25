from pathlib import Path
from typing import Callable, cast

import numpy as np
import pandas as pd

from ..cli import input_option, input_str, provide_serials
from ..constants import ValidateDataFn
from ..data import DataStore, DataStream, print_stream, read
from ..errors import Result, Unit, eprint
from ..paths import get_paths_excel
from ..result_collate import recollate
from ..result_utils import (
    det_assessment_req_col,
    det_attendance_req_col,
    det_passmark_col,
    find_col,
    val_result_data,
)


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
    result_path: Path = get_paths_excel()["Result"]
    if not result_path.exists():
        msg = "Results has not been generated yet. Please collate results before running this operation"
        eprint(msg)
        return Result.err(msg)

    result_data = read(result_path)
    if result_data.is_err():
        return result_data.propagate()
    result_data = result_data.unwrap()

    result_stream: DataStream[pd.DataFrame] = DataStream(
        result_data, cast(ValidateDataFn, val_result_data)
    )
    result_data = result_stream()

    serials = provide_serials(ds)
    if serials.is_err():
        return serials.propagate()

    serials = serials.unwrap()

    for serial in serials:
        idx = serial - 1
        print_stream(result_stream, [serial])

        mutable_cols: list[str] = get_mutable_cols(result_stream)
        proc_value: float | None = None
        column: str = ""

        while proc_value is None:
            result = input_option(mutable_cols, "Result Cols to Edit")
            if result.is_err():
                return result.propagate()
            _, column = result.unwrap()
            result = input_str(f"Enter the new value for {column}: ", lower_case=False)
            if result.is_err():
                return result.propagate()
            proc_value = _preprocess(result_stream, column, result.unwrap())
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

    return recollate(DataStream(result_data)).to_excel(result_path)
