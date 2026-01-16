from pathlib import Path

import numpy as np
import pandas as pd

from ..cli import input_path
from ..constants import SERIAL
from ..data import DataStream, read
from ..errors import Result, Unit, eprint
from ..history import History, record_assessment
from ..info import printpass
from ..paths import get_paths_excel
from ..result_utils import (
    det_assessment_req_col,
    det_assessment_score_col,
    input_marks_req,
    val_attendance_data,
)


def val_assessment_data(test_data: pd.DataFrame) -> bool:
    """Validate the input data for the assessment spreadsheet. The assessment spreadsheet should have either of the two (2) formats:
        - 2-column: Serial Number | Score
        - 3-column: Serial Number | Student Name | Score
    Note: Student names must match existing data in spelling and casing.
    If the assessment spreadsheet does not match the above formats, return False.

    :param test_data: (pd.DataFrame) - The input data to validate
    :type test_data: pd.DataFrame

    :return: (bool) - True if the input data is valid, False otherwise
    :rtype: bool
    """

    columns_list: list[str] = test_data.columns.tolist()
    match len(columns_list):
        case 2:
            scores: pd.DataFrame = test_data.select_dtypes(include=[np.number])
            names: pd.DataFrame = test_data.select_dtypes(exclude=[np.number])
            score_cols = scores.columns.tolist()
            name_cols = names.columns.tolist()
            if len(score_cols) != 1:
                return False
            if len(name_cols) != 1:
                return False
            name_list: list[str] = names.astype(str).iloc[:, 0].tolist()
            return all(name.strip() != "" for name in name_list)
        case 3:
            result = test_data.select_dtypes(include=[np.number])
            result_cols = result.columns.tolist()
            num_cols = columns_list[0], columns_list[-1]
            if len(result_cols) != len(num_cols):
                return False
            return all(col1 == col2 for col1, col2 in zip(num_cols, result_cols))
        case _:
            return False


def collate_assessment(history: History) -> Result[Unit]:
    """
    Collate the assessment spreadsheet for the students. Prompts for the user to enter a path
    to the assessment spreadsheet.

    The assessment spreadsheet should have either of the two (2) formats:
        - 2-column: Serial Number | Score
        - 3-column: Serial Number | Student Name | Score
    Note: Student names must match existing data in spelling and casing.

    If the assessment spreadsheet does not match the above formats, a SpreadSheetFmtErr will be raised.

    :param history: (History) - The state of the application
    :type history: History

    :return: (Result[Unit]) - result
    :rtype: Result[Unit]

    :raises SpreadSheetFmtErr: If the assessment spreadsheet does not match the above formats
    """
    # Check if the attendance has been collated
    if not history.has_collated_attendance:
        msg = "Please collate the attendance first before collating the assessment.\n"
        eprint(msg)
        return Result.err(msg)

    # Read the data from the attendance spreadsheet
    attendance_data = read(get_paths_excel()["Attendance"])
    if attendance_data.is_err():
        return attendance_data.propagate()
    attendance_data = attendance_data.unwrap()
    attendance = DataStream(attendance_data, val_attendance_data)
    data: pd.DataFrame = attendance()

    # Prompt the user to enter the path to the assessment spreadsheet
    msg: str = """Please enter the (absolute) path to the Excel file in one of the following formats:
    2-column: Serial Number | Score
    3-column: Serial Number | Student Name | Score
Note: Scores must be between 0 and 100.
Note: Student names must match existing data in spelling and casing.

Enter the path:  """

    # Get the path to the assessment spreadsheet from the user
    result = input_path(msg)
    if result.is_err():
        return result.propagate()
    path = result.unwrap()

    assessment_df = read(path)
    if assessment_df.is_err():
        return assessment_df.propagate()
    assessment_df = assessment_df.unwrap()

    assessment_stream: DataStream[pd.DataFrame] = DataStream(
        assessment_df, val_assessment_data
    )
    assessment_df = assessment_stream()

    # Prompt the user to enter the assessment requirement
    req = input_marks_req("Enter the Assessment Requirement [1 - 100]: ")
    if req.is_err():
        return req.propagate()
    req = req.unwrap()

    # Get the columns of the assessment spreadsheet
    assessment_cols: list[str] = assessment_df.columns.tolist()

    # Sort the assessment spreadsheet by the first column
    assessment_df = assessment_df.sort_values(by=[assessment_cols[0]])

    # Get the last column of the assessment spreadsheet
    score_col: str = assessment_cols[-1]

    # Get the serials of the assessment spreadsheet
    assessment_serials: list[int] = assessment_df.iloc[:, 0].astype(int).tolist()

    # Get the scores of the assessment spreadsheet
    assessment_scores: list[float] = (
        assessment_df.loc[:, score_col].astype(float).tolist()
    )

    serials = data[SERIAL].astype(int).tolist()

    # Get the records of the assessment spreadsheet
    assessment_records: list[float] = [
        0.0
        if serial not in assessment_serials
        else assessment_scores[assessment_serials.index(serial)]
        for serial in serials
    ]

    # Get the name of the assessment score column
    assessment_score_col: str = det_assessment_score_col()

    # Get the name of the assessment requirement column
    assessment_req_col: str = det_assessment_req_col()

    # Set the assessment scores of the attendance spreadsheet
    data[assessment_score_col] = np.array(assessment_records, dtype=np.float64).round(2)

    # Set the assessment requirement of the attendance spreadsheet
    data[assessment_req_col] = req
    printpass("Assessment recorded successfully\n")

    # Get the path to the assessment spreadsheet
    assessment_path: Path = get_paths_excel()["Assessment"]

    # Write the attendance spreadsheet to the assessment spreadsheet
    result = DataStream(data).to_excel(assessment_path)
    if result.is_err():
        return result.propagate()

    # Record the assessment in the history
    record_assessment(history)

    return Result.unit()
