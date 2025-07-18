import pandas as pd

from pylms.constants import NAME, SERIAL
from pylms.lms.utils import (
    det_assessment_req_col,
    det_attendance_req_col,
    det_result_col,
)
from pylms.lms.utils.col_name import (
    det_assessment_score_col,
    det_attendance_score_col,
)


def val_attendance_data(test_data: pd.DataFrame) -> bool:
    column_list: list[str] = test_data.columns.tolist()
    req_columns: list[str] = [SERIAL, NAME, det_attendance_score_col()]
    return all([req_column in column_list for req_column in req_columns])


def val_assessment_data(test_data: pd.DataFrame) -> bool:
    column_list: list[str] = test_data.columns.tolist()
    req_columns: list[str] = [
        SERIAL,
        NAME,
        det_attendance_score_col(),
        det_assessment_score_col(),
    ]
    return all([req_column in column_list for req_column in req_columns])


def val_result_data(test_data: pd.DataFrame) -> bool:
    columns: list[str] = test_data.columns.tolist()
    required_cols: list[str] = [
        SERIAL,
        NAME,
        det_assessment_req_col(),
        det_attendance_req_col(),
        det_result_col(),
    ]
    return all([col in columns for col in required_cols])