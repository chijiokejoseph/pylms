from pylms.data import new_validator

from ..constants import NAME, SERIAL
from .col_name import (
    det_assessment_req_col,
    det_assessment_score_col,
    det_attendance_req_col,
    det_attendance_score_col,
    det_result_col,
)

val_attendance_data = new_validator(
    [
        SERIAL,
        NAME,
        det_attendance_score_col(),
        det_attendance_req_col(),
    ]
)

val_assessment_data = new_validator(
    [
        SERIAL,
        NAME,
        det_assessment_score_col(),
        det_assessment_req_col(),
    ]
)

val_result_data = new_validator(
    [
        SERIAL,
        NAME,
        det_attendance_req_col(),
        det_assessment_req_col(),
        det_result_col(),
    ]
)

# def val_attendance_data(test_data: pl.DataFrame) -> tuple[bool, str]:
#     """Validate attendance data format.

#     Args:
#         test_data (pl.DataFrame): Attendance data to validate.

#     Returns:
#         bool: True if data contains required attendance columns.
#     """
#     column_list = test_data.columns
#     req_columns = [SERIAL, NAME, det_attendance_score_col()]
#     missing_cols = [column for column in column_list if column not in req_columns]

#     if len(missing_cols) > 0


# def val_assessment_data(test_data: pl.DataFrame) -> bool:
#     """Validate assessment data format.

#     Args:
#         test_data (pl.DataFrame): Assessment data to validate.

#     Returns:
#         bool: True if data contains required assessment columns.
#     """
#     column_list = test_data.columns
#     req_columns = [
#         SERIAL,
#         NAME,
#         det_attendance_score_col(),
#         det_assessment_score_col(),
#     ]
#     return all([req_column in column_list for req_column in req_columns])


# def val_result_data(test_data: pl.DataFrame) -> bool:
#     """Validate result data format.

#     Args:
#         test_data (pl.DataFrame): Result data to validate.

#     Returns:
#         bool: True if data contains required result columns.
#     """
#     columns = test_data.columns
#     required_cols = [
#         SERIAL,
#         NAME,
#         det_assessment_req_col(),
#         det_attendance_req_col(),
#         det_result_col(),
#     ]
#     return all([col in columns for col in required_cols])
