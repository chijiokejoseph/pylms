from pathlib import Path
from typing import cast

import pandas as pd

from pylms.constants import RESULT_UPDATE, ValidateDataFn
from pylms.lms.collate.errors import IntConvertErr, NonExistentPathErr
from pylms.lms.edit.select import Select, input_select_type
from pylms.lms.edit.edit_for_all import _edit_all
from pylms.lms.edit.edit_for_multiple import _edit_mutliple
from pylms.lms.edit.edit_for_batch import _edit_batch
from pylms.lms.utils import val_result_data
from pylms.utils import DataStore, DataStream, paths, read_data


NUM_LAST_COLS: int = 2
LAST_COLS: list[str] = [
    "Result [100%]",
    "Result Req",
    "Remarks",
    "Reason",
]


def edit_result(ds: DataStore) -> None:
    result_path: Path = paths.get_paths_excel()["Result"]
    if not result_path.exists():
        raise NonExistentPathErr(
            "Results has not been generated yet. Please collate results before running this operation"
        )

    result_data: pd.DataFrame = read_data(result_path)
    result_stream: DataStream[pd.DataFrame] = DataStream(
        result_data, cast(ValidateDataFn, val_result_data)
    )
    result_data = result_stream()

    result_cols: list[str] = result_data.columns.tolist()
    first_unchanged_idx: int = len(result_cols) - NUM_LAST_COLS
    print(f"{len(result_cols) = }")
    print(f"{result_cols = }")
    print(f"{first_unchanged_idx = }")
    stop_idx: int = first_unchanged_idx

    for idx, each_col in enumerate(result_cols):
        if each_col.startswith(RESULT_UPDATE):
            stop_idx = idx
            break

    print(f"{stop_idx = }")
    update_num: int = 1
    for idx, each_col in enumerate(result_cols[stop_idx:first_unchanged_idx]):
        if each_col.startswith(RESULT_UPDATE):
            num_str = each_col.replace(RESULT_UPDATE, "").strip()
            try:
                num: int = int(num_str)
            except ValueError:
                raise IntConvertErr(
                    "Err when getting the last result update number in the process of editing a student's result record"
                )
            update_num = num + 1

    select_type: Select = input_select_type()
    updates_list: list[float] = []
    match select_type:
        case Select.ALL:
            updates_list.extend(_edit_all(result_data))
        case Select.MULTIPLE:
            updates_list.extend(_edit_mutliple(ds, result_data))
        case Select.BATCH:
            updates_list.extend(_edit_batch(ds, result_data))

    unchanged_cols: list[str] = result_cols[:first_unchanged_idx]
    remaining_cols: list[str] = result_cols[first_unchanged_idx:]
    new_col = RESULT_UPDATE + f" {update_num}"
    result_data[new_col] = updates_list
    result_data = result_data[unchanged_cols + [new_col] + remaining_cols]
    result_stream = DataStream(result_data)
    result_stream.to_excel(paths.get_paths_excel()["Result"])
