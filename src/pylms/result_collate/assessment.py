import polars as pl

from ..cli import input_path
from ..config import Config
from ..constants import NAME, SERIAL
from ..data import DataStream, read, write
from ..errors import Result, Unit, eprint
from ..history import History, record_assessment
from ..info import printpass
from ..paths import get_paths_excel
from ..result_utils import (
    det_assessment_req_col,
    det_assessment_score_col,
    input_marks_req,
    val_assessment_in,
    val_attendance_data,
)


def collate_assessment(config: Config, history: History) -> Result[Unit]:
    """Collate assessment spreadsheet for students.

    Prompts user for assessment spreadsheet path and processes scores.
    Assessment spreadsheet should have either:
    - 2-column: Serial Number | Score
    - 3-column: Serial Number | Student Name | Score

    Args:
        config (Config): Application configuration.
        history (History): Application state tracking.

    Returns:
        Result[Unit]: Success or error with message.
    """
    # Check if attendance has been collated
    if not history.has_collated_attendance:
        msg = "Please collate the attendance first before collating the assessment.\n"
        eprint(msg)
        return Result.err(msg)

    paths = get_paths_excel(config)
    # Read attendance data
    attendance = read(paths["Attendance"])
    if attendance.is_err():
        return attendance.propagate()
    attendance = attendance.unwrap()

    result = DataStream.verify(attendance, val_attendance_data)
    if result.is_err():
        return result.propagate()

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

    assessment = read(path)
    if assessment.is_err():
        return assessment.propagate()
    assessment = assessment.unwrap()

    result = DataStream.verify(assessment, val_assessment_in)
    if result.is_err():
        return result.propagate()

    # Get assessment requirement
    req = input_marks_req("Enter the Assessment Requirement [1 - 100]: ")
    if req.is_err():
        return req.propagate()
    req = req.unwrap()

    # Get assessment columns
    assessment_cols = assessment.columns

    # Sort by first column
    assessment = assessment.sort(assessment_cols[0])

    # Get score column (last column)
    score_col = assessment_cols[-1]

    # Get column names
    assessment_score_col = det_assessment_score_col()
    assessment_req_col = det_assessment_req_col()

    # Update data with assessment scores and requirement
    final_assessment = (
        attendance.join(
            assessment,
            on=[SERIAL, NAME],
        )
        .fill_null(0.0)
        .with_columns(
            pl.col(score_col).round(2).alias(assessment_score_col),
            pl.lit(req).alias(assessment_req_col),
        )
        .drop(score_col)
    )

    printpass("Assessment recorded successfully\n")

    # Save to Excel
    assessment_path = paths["Assessment"]
    result = write(final_assessment, assessment_path)
    if result.is_err():
        return result.propagate()

    # Record in history
    record_assessment(config, history)

    return Result.unit()
