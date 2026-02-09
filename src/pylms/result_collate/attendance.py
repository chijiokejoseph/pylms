import polars as pl

from ..constants import COMMA_DELIM, NAME, SERIAL
from ..data import DataStore, write
from ..errors import Result, Unit, eprint
from ..history import (
    History,
    get_held_classes,
    get_unrecorded_classes,
    record_attendance,
)
from ..info import printpass
from ..paths import get_paths_excel
from ..record import RecordStatus
from ..result_utils import (
    det_attendance_req_col,
    det_attendance_score_col,
    det_attendance_total_col,
    input_marks_req,
)


def collate_attendance(ds: DataStore, history: History) -> Result[Unit]:
    """Collate attendance spreadsheet for students.

    Processes attendance data for all held classes and calculates attendance scores.
    Saves collated data to Attendance.xlsx file.

    Args:
        ds (DataStore): Student data to be collated.
        history (History): Application state tracking.

    Returns:
        Result[Unit]: Success or error with message.
    """
    # Extract dates of classes that were held
    held_dates = get_held_classes(history, "")
    unrecorded_dates = get_unrecorded_classes(history, "")

    # Check if all attendance records are complete
    if len(unrecorded_dates) > 0:
        dates_print = COMMA_DELIM.join(unrecorded_dates)
        msg = f"Dates: {dates_print} have been held but have not been marked yet. Please mark before collating attendance"
        eprint(msg)
        return Result.err(msg)

    # Retrieve and filter relevant data for held classes
    pretty = ds.pretty()
    data = ds.as_ref()
    dates_data = data.select(held_dates)

    # Get attendance requirement from user
    req = input_marks_req("Enter the Attendance Requirement [1 - 100]: ")
    if req.is_err():
        return req.propagate()
    req = req.unwrap()

    # Calculate attendance counts per student
    count_data = dates_data.with_columns(
        [
            pl.when(pl.col(col) == str(RecordStatus.ABSENT))
            .then(0)
            .otherwise(1)
            .alias(col)
            for col in held_dates
        ]
    )
    count_arr = count_data.sum_horizontal().to_numpy()

    # Calculate attendance scores
    num_classes_held = len(held_dates)
    score_arr = (count_arr * 100 / num_classes_held).round(2)

    # Determine column names
    total_col = det_attendance_total_col(num_classes_held)
    score_col = det_attendance_score_col()
    req_col = det_attendance_req_col()

    # Create collated attendance DataFrame
    collated_data = pl.DataFrame(
        {
            SERIAL: data[SERIAL],
            NAME: pretty[NAME],
            total_col: count_arr,
            score_col: score_arr,
            req_col: pl.lit(req),
        }
    )

    printpass("Attendance recorded successfully\n")

    # Save to Excel file
    path = get_paths_excel()["Attendance"]
    result = write(collated_data, path)
    if result.is_err():
        return result.propagate()

    # Record in history
    record_attendance(history)

    return Result.unit()
