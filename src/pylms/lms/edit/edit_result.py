from pathlib import Path
from typing import cast

import pandas as pd

from pylms.constants import RESULT_UPDATE, ValidateDataFn
from pylms.errors import Result, Unit
from pylms.lms.edit.edit_for_all import edit_all
from pylms.lms.edit.edit_for_batch import edit_batch
from pylms.lms.edit.edit_for_multiple import edit_multiple
from pylms.lms.edit.select import Select, input_select_type
from pylms.lms.utils import val_result_data
from pylms.lms.utils.find import find_col
from pylms.utils import DataStore, DataStream, paths, read_data


def edit_result(ds: DataStore) -> Result[Unit]:
    """
    Edit student result records in the result Excel file.

    :param ds: (DataStore) - The DataStore object used for managing and accessing data throughout the operation.
    :type ds: DataStore

    :return: (Result[Unit]) - A Result object indicating success or failure of the operation.
        On success, it contains a Unit value. On failure, it contains an error message.
    :rtype: Result[Unit]

    Caught Exceptions:
        - FileNotFoundError: If the result file does not exist (i.e., results have not been generated yet).
        - PermissionError: If there is an error reading the result file, possibly because it is open in another program.
        - ValueError: If there is an error converting the result update number to an integer when determining the next update column.


    This function allows the user to update student result records by adding a new result update column to the result Excel file. It supports editing all records, multiple records, or a batch of records, depending on the user's selection. The function ensures that the result file exists, loads the data, determines the next update column, and applies the updates accordingly. The new result update column is added, and the updated data is saved back to the result Excel file.
    """
    # Check if the result file exists
    result_path: Path = paths.get_paths_excel()["Result"]
    # If the result file does not exist, raise an error
    if not result_path.exists():
        msg: str = "Results has not been generated yet. Please collate results before running this operation"
        print(msg)
        return Result[Unit].err(FileNotFoundError(msg))

    # Load the result data from the Excel file
    try:
        result_data: pd.DataFrame = read_data(result_path)
    except PermissionError as e:
        print(f"Error reading file at {result_path} as it is open in another program.")
        return Result[Unit].err(e)
    # Validate the result data
    result_stream: DataStream[pd.DataFrame] = DataStream(
        result_data, cast(ValidateDataFn, val_result_data)
    )
    # Get the validated result data
    result_data = result_stream()

    # Determine the next result update column
    result_cols: list[str] = result_data.columns.tolist()
    result_col: str = find_col(result_stream, "Result", "Score")
    result_col_idx: int = result_cols.index(result_col)
    last_col_idx: int = result_col_idx - 1
    last_col = result_cols[last_col_idx]

    update_num: int = 1
    if last_col.startswith(RESULT_UPDATE):
        last_col_num: str = last_col.replace(RESULT_UPDATE, "").strip()
        try:
            update_num = int(last_col_num) + 1
        except ValueError as e:
            print(
                "Error when getting the last result update number in the process of editing a student's result record"
            )
            return Result[Unit].err(e)

    # Get the type of edit to perform (all, multiple, or batch)
    select_result = input_select_type()
    if select_result.is_err():
        return Result[Unit].err(select_result.unwrap_err())
    select_type: Select = select_result.unwrap()
    updates_list: list[float] = []

    # Perform the selected edit operation
    match select_type:
        case Select.ALL:
            result = edit_all(result_data)
            if result.is_err():
                return Result[Unit].err(result.unwrap_err())
            updates_list.extend(result.unwrap())
        case Select.MULTIPLE:
            result = edit_multiple(ds, result_data)
            if result.is_err():
                return Result[Unit].err(result.unwrap_err())
            updates_list.extend(result.unwrap())
        case Select.BATCH:
            result = edit_batch(ds, result_data)
            if result.is_err():
                return Result[Unit].err(result.unwrap_err())
            updates_list.extend(result.unwrap())

    # Reorder columns to place the new result update column correctly
    unchanged_cols: list[str] = result_cols[: last_col_idx + 1]
    remaining_cols: list[str] = result_cols[last_col_idx + 1 :]
    # Set the new result update column
    new_col = RESULT_UPDATE + f" {update_num}"
    # Add the new result update column and save the updated data
    result_data[new_col] = updates_list
    result_data = result_data[unchanged_cols + [new_col] + remaining_cols]
    result_stream = DataStream(result_data)
    result_stream.to_excel(paths.get_paths_excel()["Result"])
    return Result[Unit].unit()
