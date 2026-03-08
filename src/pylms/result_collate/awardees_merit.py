from typing import Literal

import numpy as np
import polars as pl

from ..config import Config
from ..constants import (
    COHORT,
    FAIL,
    PASS,
    REASON,
    REMARK,
)
from ..data import DataStore, DataStream, read, write
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
"""Type alias for merit collation types."""


def collate_merit(config: Config, ds: DataStore, history: History) -> Result[Unit]:
    """Collate merit-based results and generate awardees list.

    Processes student results to determine pass/fail status based on multiple criteria
    including assessment scores, attendance, and special considerations.

    Args:
        config (Config): Application configuration.
        ds (DataStore): DataStore containing student data.
        history (History): Application state tracking.

    Returns:
        Result[Unit]: Success or error with message.
    """
    paths = get_paths_excel(config)
    results = read(paths["Result"])
    if results.is_err():
        return results.propagate()
    results = results.unwrap()

    results_stream = DataStream.new(results, val_result_data)
    if results_stream.is_err():
        return results_stream.propagate()

    results_stream = results_stream.unwrap()
    results = results_stream.as_ref()

    attendance_score_col = det_attendance_score_col()
    assessment_score_col = find_col(results_stream, "Assessment", "Score")
    if assessment_score_col.is_err():
        return assessment_score_col.propagate()
    assessment_score_col = assessment_score_col.unwrap()

    attendance_count_col = find_col(results_stream, "Attendance", "Count")
    if attendance_count_col.is_err():
        return attendance_count_col.propagate()
    attendance_count_col = attendance_count_col.unwrap()

    attendance_count = find_count(attendance_count_col)
    if attendance_count is None:
        msg = f"Expected an integer count in col {attendance_count_col}"
        eprint(msg)
        return Result.err(msg)

    excellent_attendance_count = attendance_count - 1
    attendance_req_col = det_attendance_req_col()
    assessment_req_col = det_assessment_req_col()
    result_col = det_result_col()
    passmark_col = det_passmark_col()

    # Get requirement values
    attendance_req = results[0, attendance_req_col]
    assessment_req = results[0, assessment_req_col]
    passmark = results[0, passmark_col]

    # Calculate pass criteria using Polars expressions
    attendance_cond = pl.col(attendance_score_col) >= attendance_req
    assessment_cond = pl.col(attendance_count_col) >= assessment_req
    score_cond = pl.col(result_col) >= passmark
    near_score = (pl.col(result_col) >= passmark - 5) & (pl.col(result_col) < passmark)
    excellent_attendance = pl.col(attendance_score_col) >= np.round(
        excellent_attendance_count * 100 / attendance_count, 1
    )
    near_attendance = (pl.col(attendance_score_col) >= 50) & (
        pl.col(attendance_score_col) < attendance_req
    )
    excellent_score = pl.col(result_col) >= passmark + 10

    pass_cond = assessment_cond & (
        (attendance_cond & score_cond)
        | (near_score & excellent_attendance)
        | (near_attendance & excellent_score)
    )

    # Evaluate Reasons and Remark Based on Pass Criteria
    results = results.lazy()
    results = (
        results.with_columns(
            [
                pl.when(assessment_cond)
                .then(pl.lit("You passed the assessment"))
                .otherwise(pl.lit("You failed the assessment"))
                .alias(REASON + "1"),
                pl.when(attendance_cond | (near_attendance & excellent_score))
                .then(pl.lit("You met the attendance requirement"))
                .otherwise(pl.lit("You failed to meet the attendance requirement"))
                .alias(REASON + "2"),
                pl.when(score_cond | (near_score & excellent_attendance))
                .then(pl.lit("You met the passmark"))
                .otherwise(pl.lit("You failed to meet the passmark"))
                .alias(REASON + "3"),
            ]
        )
        .with_columns(
            [
                pl.concat_str(
                    [pl.col(REASON + str(i)) for i in range(1, 4)], separator="\n"
                ).alias(REASON),
                pl.when(pass_cond)
                .then(pl.lit(PASS))
                .otherwise(pl.lit(FAIL))
                .alias(REMARK),
            ]
        )
        .collect()
    )
    results = results.drop([REASON + str(i) for i in range(1, 4)])
    pass_series = results.with_columns(
        pl.when(pass_cond).then(pl.lit(True)).otherwise(pl.lit(False)).alias("Cond")
    )["Cond"]

    # Save updated results
    result_path = paths["Result"]
    results = write(results, result_path)
    if results.is_err():
        return results.propagate()

    pretty = ds.pretty()
    passed_data = pretty.filter(pass_series)
    passed_stream = DataStream(passed_data)
    cohort = pretty[0, COHORT]

    results = collate_awardees(config, passed_stream, cohort)
    if results.is_err():
        return results.propagate()

    results = record_merit(config, history)
    if results.is_err():
        return results.propagate()

    return Result.unit()
