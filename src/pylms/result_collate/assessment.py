from pathlib import Path

import numpy as np
import polars as pl

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


def val_assessment_data(test_data: pl.DataFrame) -> bool:
    """Validate assessment spreadsheet format.
    
    Assessment spreadsheet should have either:
    - 2-column: Serial Number | Score
    - 3-column: Serial Number | Student Name | Score
    
    Args:
        test_data (pl.DataFrame): Assessment data to validate.
        
    Returns:
        bool: True if data format is valid, False otherwise.
    """
    columns_list = test_data.columns
    match len(columns_list):
        case 2:
            # Check for one numeric and one non-numeric column
            numeric_cols = [col for col in columns_list if test_data[col].dtype.is_numeric()]
            string_cols = [col for col in columns_list if not test_data[col].dtype.is_numeric()]
            
            if len(numeric_cols) != 1 or len(string_cols) != 1:
                return False
                
            # Check that string column has non-empty values
            string_col = string_cols[0]
            name_list = test_data[string_col].cast(pl.Utf8).to_list()
            return all(name.strip() != "" for name in name_list)
        case 3:
            # Check that first and last columns are numeric
            first_col = columns_list[0]
            last_col = columns_list[-1]
            return (test_data[first_col].dtype.is_numeric() and 
                   test_data[last_col].dtype.is_numeric())
        case _:
            return False


def collate_assessment(history: History) -> Result[Unit]:
    """Collate assessment spreadsheet for students.
    
    Prompts user for assessment spreadsheet path and processes scores.
    Assessment spreadsheet should have either:
    - 2-column: Serial Number | Score  
    - 3-column: Serial Number | Student Name | Score
    
    Args:
        history (History): Application state tracking.
        
    Returns:
        Result[Unit]: Success or error with message.
    """
    # Check if attendance has been collated
    if not history.has_collated_attendance:
        msg = "Please collate the attendance first before collating the assessment.\n"
        eprint(msg)
        return Result.err(msg)

    # Read attendance data
    attendance_data = read(get_paths_excel()["Attendance"])
    if attendance_data.is_err():
        return attendance_data.propagate()
    attendance_data = attendance_data.unwrap()
    attendance = DataStream(attendance_data, val_attendance_data)
    data = attendance.as_ref()

    # Prompt for assessment spreadsheet path
    msg = """Please enter the (absolute) path to the Excel file in one of the following formats:
    2-column: Serial Number | Score
    3-column: Serial Number | Student Name | Score
Note: Scores must be between 0 and 100.
Note: Student names must match existing data in spelling and casing.

Enter the path:  """

    result = input_path(msg)
    if result.is_err():
        return result.propagate()
    path = result.unwrap()

    assessment_df = read(path)
    if assessment_df.is_err():
        return assessment_df.propagate()
    assessment_df = assessment_df.unwrap()

    assessment_stream = DataStream(assessment_df, val_assessment_data)
    assessment_df = assessment_stream.as_ref()

    # Get assessment requirement
    req = input_marks_req("Enter the Assessment Requirement [1 - 100]: ")
    if req.is_err():
        return req.propagate()
    req = req.unwrap()

    # Get assessment columns
    assessment_cols = assessment_df.columns

    # Sort by first column
    assessment_df = assessment_df.sort(assessment_cols[0])

    # Get score column (last column)
    score_col = assessment_cols[-1]

    # Get serials and scores
    assessment_serials = assessment_df[assessment_cols[0]].cast(pl.Int32).to_list()
    assessment_scores = assessment_df[score_col].cast(pl.Float64).to_list()

    serials = data[SERIAL].cast(pl.Int32).to_list()

    # Map scores to serials
    assessment_records = [
        0.0
        if serial not in assessment_serials
        else assessment_scores[assessment_serials.index(serial)]
        for serial in serials
    ]

    # Get column names
    assessment_score_col = det_assessment_score_col()
    assessment_req_col = det_assessment_req_col()

    # Update data with assessment scores and requirement
    data = data.with_columns([
        pl.Series(assessment_score_col, assessment_records).round(2),
        pl.lit(req).alias(assessment_req_col)
    ])
    
    printpass("Assessment recorded successfully\n")

    # Save to Excel
    assessment_path = get_paths_excel()["Assessment"]
    result = DataStream(data).to_excel(assessment_path)
    if result.is_err():
        return result.propagate()

    # Record in history
    record_assessment(history)

    return Result.unit()
