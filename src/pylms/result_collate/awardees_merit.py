from typing import Literal

import pandas as pd

from ..constants import (
    FAIL,
    PASS,
    REASON,
    REMARK,
)
from ..data import DataStore, DataStream, read
from ..errors import Result, Unit, eprint
from ..history import History, record_merit
from ..paths import get_paths_excel
from ..result_utils import (
    det_assessment_req_col,
    det_attendance_req_col,
    det_attendance_score_col,
    det_passmark_col,
    det_result_col,
    find_col,
    find_count,
    val_result_data,
)
from .awardees import collate_awardees

type CollateType = Literal["merit", "fast track"]


def remark(
    assessment_pass: list[bool],
    special_score_pass: list[bool],
    special_attendance_pass: list[bool],
    standard_attendance_pass: list[bool],
    standard_score_pass: list[bool],
) -> tuple[list[str], list[str]]:
    remarks: list[str] = []
    reasons: list[str] = []
    for assessment, special_score, special_attendance, attendance, score in zip(
        assessment_pass,
        special_score_pass,
        special_attendance_pass,
        standard_attendance_pass,
        standard_score_pass,
    ):
        score_pass: bool = special_score or special_attendance or (attendance and score)
        passed: bool = assessment and score_pass
        remark: str = PASS if passed else FAIL
        reason: str = ""
        if not assessment:
            reason += "You failed the assessment; "
        else:
            reason += "You passed the assessment; "
        if not score_pass:
            if not score:
                reason += "You did not meet the passmark; "
            if not attendance:
                reason += "You did not meet the attendance requirement; "
        else:
            reason += (
                "You met the passmark and your attendance was deemed satisfactory; "
            )
        remarks.append(remark)
        reasons.append(reason)
    return remarks, reasons


def collate_merit(ds: DataStore, history: History) -> Result[Unit]:
    result_data = read(get_paths_excel()["Result"])
    if result_data.is_err():
        return result_data.propagate()
    result_data = result_data.unwrap()

    result_stream = DataStream(result_data, val_result_data)
    result_data = result_stream()

    attendance_score_col: str = det_attendance_score_col()
    result = find_col(result_stream, "Assessment", "Score")
    if result.is_err():
        return result.propagate()
    assessment_score_col: str = result.unwrap()

    result = find_col(result_stream, "Attendance", "Count")
    if result.is_err():
        return result.propagate()
    attendance_count_col: str = result.unwrap()

    attendance_count: int | None = find_count(attendance_count_col)
    if attendance_count is None:
        msg = f"Expected an integer count in col {attendance_count_col}"
        eprint(msg)
        return Result.err(msg)

    excellent_attendance_count: int = attendance_count - 1
    attendance_req_col: str = det_attendance_req_col()
    assessment_req_col: str = det_assessment_req_col()
    result_col: str = det_result_col()
    passmark_col: str = det_passmark_col()

    # logical indices for meeting attendance requirement
    attendance_pass: pd.Series = (
        result_data[attendance_score_col] >= result_data[attendance_req_col].loc[0]
    )

    # logical indices for meeting assessment requirement
    assessment_pass: pd.Series = (
        result_data[assessment_score_col] >= result_data[assessment_req_col].loc[0]
    )

    # logical indices for meeting passmark requirement
    score_pass: pd.Series = result_data[result_col] >= result_data[passmark_col].loc[0]

    # special pleading for excellent attendance but almost passmark scores
    near_score_pass: pd.Series = (
        result_data[result_col] >= result_data[passmark_col].loc[0] - 5
    ) & (
        result_data[result_col] < result_data[passmark_col].loc[0]
    )  # scores are within 5 marks from the passmark ❌
    excellent_attendance: float = excellent_attendance_count * 100 / attendance_count
    brilliant_attendance_pass: pd.Series = (
        result_data[attendance_score_col] >= excellent_attendance
    )  # attendance is excellent ✅

    # special pleading for excellent scores but poor attendance
    poor_attendance_pass: pd.Series = (result_data[attendance_score_col] >= 50) & (
        result_data[attendance_score_col] < result_data[attendance_req_col].loc[0]
    )  # attendance is at least 50 but not up to the requirement ❌
    excellent_score: float = result_data[passmark_col].loc[0] + 10
    brilliant_score_pass: pd.Series = (
        result_data[result_col] >= excellent_score
    )  # scores are excellent ✅

    attendance_score_pass: pd.Series = (
        (near_score_pass & brilliant_attendance_pass)
        | (poor_attendance_pass & brilliant_score_pass)
        | (attendance_pass & score_pass)
    )

    remarks, reasons = remark(
        assessment_pass.tolist(),
        (poor_attendance_pass & brilliant_score_pass).tolist(),
        (brilliant_attendance_pass & near_score_pass).tolist(),
        attendance_pass.tolist(),
        score_pass.tolist(),
    )
    result_data[REMARK] = remarks
    result_data[REASON] = reasons
    DataStream(result_data).to_excel(get_paths_excel()["Result"])

    pass_logic_idx: pd.Series = attendance_score_pass & assessment_pass
    pretty_data: pd.DataFrame = ds.pretty()
    passed_data: pd.DataFrame = pretty_data.loc[pass_logic_idx, :]
    passed_stream: DataStream[pd.DataFrame] = DataStream(passed_data)

    result = collate_awardees(passed_stream)
    if result.is_err():
        return result.propagate()

    result = record_merit(history)
    if result.is_err():
        return result.propagate()

    return Result.unit()
