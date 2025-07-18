from typing import Literal, cast

import pandas as pd

from pylms.constants import (
    ValidateDataFn,
)
from pylms.lms.collate.awardees import collate_awardees
from pylms.lms.collate.errors import SpreadSheetFmtErr
from pylms.lms.utils import (
    det_assessment_req_col,
    det_attendance_req_col,
    det_attendance_score_col,
    det_passmark_col,
    det_result_col,
    find_col,
    find_count,
    val_result_data,
)
from pylms.utils import DataStore, DataStream, paths, read_data

type CollateType = Literal["merit", "fast track"]


def collate_merit(ds: DataStore) -> None:
    result_data: pd.DataFrame = read_data(paths.get_paths_excel()["Result"])
    result_stream = DataStream(result_data, cast(ValidateDataFn, val_result_data))
    result_data = result_stream()

    attendance_score_col: str = det_attendance_score_col()
    assessment_score_col: str = find_col(result_stream, "Assessment", "Score")
    attendance_count_col: str = find_col(result_stream, "Attendance", "Count")
    attendance_count: int | None = find_count(attendance_count_col)
    if attendance_count is None:
        raise SpreadSheetFmtErr(
            f"Expected an integer count in col {attendance_count_col}"
        )
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
    pass_logic_idx: pd.Series = attendance_score_pass & assessment_pass
    pretty_data: pd.DataFrame = ds.pretty()
    passed_data: pd.DataFrame = pretty_data.loc[pass_logic_idx, :]
    passed_stream: DataStream[pd.DataFrame] = DataStream(passed_data)
    collate_awardees(passed_stream)
