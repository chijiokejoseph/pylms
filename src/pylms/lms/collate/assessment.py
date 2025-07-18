from pathlib import Path
from typing import Callable, cast

import numpy as np
import pandas as pd

from pylms.cli import input_path, test_path_in
from pylms.constants import SERIAL
from pylms.lms.utils import (
    det_assessment_req_col,
    det_assessment_score_col,
    val_attendance_data,
)
from pylms.utils import DataStream, read_data


def _val_input_data(test_data: pd.DataFrame) -> bool:
    columns_list: list[str] = test_data.columns.tolist()
    match len(columns_list):
        case 2:
            result: pd.DataFrame = test_data.select_dtypes(include=[np.number])
            result_cols = result.columns.tolist()
            if len(result_cols) != len(columns_list):
                return False
            return all(col1 == col2 for col1, col2 in zip(columns_list, result_cols))
        case 3:
            result = test_data.select_dtypes(include=[np.number])
            result_cols = result.columns.tolist()
            num_cols = columns_list[0], columns_list[-1]
            if len(result_cols) != len(num_cols):
                return False
            return all(col1 == col2 for col1, col2 in zip(num_cols, result_cols))
        case _:
            return False


def collate_assessment(
    data_stream: DataStream[pd.DataFrame], req: float
) -> DataStream[pd.DataFrame]:
    type ValidateFn = Callable[[pd.DataFrame | pd.Series], bool]
    validate_fn = cast(ValidateFn, val_attendance_data)
    data_stream = DataStream(data_stream(), validate_fn)
    data: pd.DataFrame = data_stream()

    msg: str = """Enter the absolute path to the assessment excel spreadsheet for the students.
The entered spreadsheet should take either of these two (2) formats:
    i. Two column spreadsheet
    ii. Three column spreadsheet

Two Column Spreadsheet:
    Here the data should have just two columns, the first column should contain the serial numbers of the students
    and the second column should contain their overall assessment scores graded to 100%.
    
Three Column Spreadsheet:
    Here the data unlike in the two columns has an extra column preceding the scores columns
    but after the serial numbers that holds the names of the students.
      
Please take note that the names of students in both cases must be spelt in the same arrangement and casing 
as the existing data.
Furthermore the entered path should be absolute and not relative.

Enter the path:  """

    path: Path = input_path(
        msg,
        path_test_fn=test_path_in,
        path_test_diagnosis="The path entered does not exist, "
        "is not absolute or is not a valid excel file.",
    )
    assessment_df: pd.DataFrame = read_data(path)
    validate_fn = cast(ValidateFn, _val_input_data)
    assessment_stream: DataStream[pd.DataFrame] = DataStream(assessment_df, validate_fn)

    assessment_df = assessment_stream()
    df_rows = assessment_df.shape[0]
    ds_rows = data.shape[0]
    if df_rows != ds_rows:
        raise
    assessment_cols: list[str] = assessment_df.columns.tolist()
    assessment_df = assessment_df.sort_values(by=[assessment_cols[0]])
    score_col: str = assessment_cols[-1]
    assessment_serials: pd.Series = assessment_df.iloc[:, 0]
    assessment_scores: pd.Series = assessment_df.loc[:, score_col]

    assessment_records: list[float] = [
        score
        for score, serial in zip(assessment_scores, assessment_serials)
        if serial in data[SERIAL].tolist()
    ]

    assessment_score_col: str = det_assessment_score_col()
    assessment_req_col: str = det_assessment_req_col()
    data[assessment_score_col] = np.array(assessment_records, dtype=np.float64).round(2)
    data[assessment_req_col] = req
    print("\nAssessment recorded successfully\n")
    return DataStream(data)
