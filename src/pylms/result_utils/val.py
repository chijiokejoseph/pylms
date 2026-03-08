import polars as pl

from ..history import History, get_num_groups
from ..constants import AWARDEES, NAME, SERIAL
from ..data import new_validator
from .col_name import (
    det_assessment_req_col,
    det_assessment_score_col,
    det_attendance_req_col,
    det_attendance_score_col,
    det_project_score_col,
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


def val_assessment_in(test: pl.DataFrame) -> tuple[bool, str]:
    columns = test.columns

    match len(columns):
        case 2 | 3:
            serial_col = columns[0]
            score_col = columns[-1]
            cond1 = test[serial_col].dtype.is_integer()
            cond2 = test[score_col].dtype.is_float()

            if not cond1:
                remark = (
                    f"First Column for serials '{serial_col}' does not hold integers."
                )
                return False, remark
            if not cond2:
                remark = f"Last Column for scores '{score_col}' does not hold float."
                return False, remark

            cond3 = (test[score_col].round(2) > 100).any()
            cond4 = (test[score_col].round(2) < 0).any()
            if cond3:
                remark = "Score column contains scores greater than 100."
                return False, remark
            if cond4:
                remark = "Score column contains scores less than 100.\n"
                return False, remark

        case _:
            remark = f"Number of columns ({len(columns)}) does not match expected values of 2 | 3"
            return False, remark

    return True, ""


val_assessment_data = new_validator(
    [
        SERIAL,
        NAME,
        det_assessment_score_col(),
        det_assessment_req_col(),
    ]
)

def val_project_in(test_data: pl.DataFrame, history: History) -> tuple[bool, str]:
    columns = test_data.columns
    num_rows = test_data.height
    num_groups = get_num_groups(history)
    if num_rows != num_groups:
        msg = f"Project Groups created in the project are {num_groups} yet project scores received correspond to {num_rows} groups."
        return False, msg

    last_col = columns[-1]

    if not test_data[last_col].dtype.is_numeric():
        return False, f"Last column: '{last_col}' does not contain numbers"

    return True, ""


val_project_data = new_validator([
    SERIAL,
    NAME,
    det_attendance_req_col(),
    det_assessment_req_col(),
    det_project_score_col(),
])

val_result_data = new_validator(
    [
        SERIAL,
        NAME,
        det_attendance_req_col(),
        det_assessment_req_col(),
        det_result_col(),
    ]
)

val_awardees = new_validator(
    [
        AWARDEES["Batch"],
        AWARDEES["BatchID"],
        AWARDEES["CertID"],
        AWARDEES["CourseTitle"],
        AWARDEES["Date"],
        AWARDEES["Email"],
        AWARDEES["Name"],
        AWARDEES["Phone"],
    ]
)