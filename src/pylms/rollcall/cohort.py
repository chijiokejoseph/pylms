from datetime import datetime
from pathlib import Path

import numpy as np
import polars as pl

from ..cli import input_bool
from ..config import Config
from ..constants import COHORT, DATA_COLUMNS, DATE_FMT
from ..data import DataStore, datamap, write
from ..errors import Result, eprint
from ..history import (
    History,
    all_dates,
    get_available_cds_forms,
    get_marked_classes,
)
from ..info import print_info
from ..paths import get_cohort_path
from ..record import RecordStatus


def fill_norm_records(record_input: str) -> RecordStatus:
    """Normalize attendance records for NCAIR team review.

    Args:
        record_input (str): Input attendance record.

    Returns:
        RecordStatus: PRESENT for valid attendance, ABSENT otherwise.
    """
    if record_input in [
        RecordStatus.CDS,
        RecordStatus.EXCUSED,
        RecordStatus.PRESENT,
    ]:
        return RecordStatus.PRESENT
    else:
        return RecordStatus.ABSENT


@np.vectorize
def fill_records(record_input: str) -> str:
    """Convert string input to appropriate RecordStatus.

    Args:
        record_input (str): String representation of attendance status.

    Returns:
        RecordStatus: Corresponding RecordStatus enum value.
    """
    match str(record_input):
        case RecordStatus.PRESENT:
            return str(RecordStatus.PRESENT)
        case RecordStatus.EXCUSED:
            return str(RecordStatus.EXCUSED)
        case RecordStatus.CDS:
            return str(RecordStatus.CDS)
        case RecordStatus.NO_CLASS:
            return str(RecordStatus.NO_CLASS)
        case _:
            return str(RecordStatus.ABSENT)


def record_cohort(config: Config, ds: DataStore, history: History) -> Result[Path]:
    """Generate half-cohort attendance record for NCAIR review.

    Args:
        config (Config): Configuration object with app settings.
        ds (DataStore): DataStore containing student attendance data.
        history (History): History object with class and form information.

    Returns:
        Result[Path]: Success with path to generated file or error.
    """
    # Get DataStore data in its pretty form
    pretty = ds.pretty()

    # Get cohort number
    cohort_no = pretty[0, COHORT]

    # Get class dates
    dates = all_dates(history, "")

    today = datetime.now()
    past_classes = [
        each_date
        for each_date in dates
        if datetime.strptime(each_date, DATE_FMT) <= today
    ]
    last_class = past_classes[-1]

    # Check CDS forms status
    available_cds_forms = get_available_cds_forms(history)
    if len(available_cds_forms) != 0 and len(history.recorded_cds_forms) > 0:
        msg = "Cannot record half cohort attendance since the CDS days of the NYSC students has not yet been recorded. Please record the CDS days then try again."
        print_info(msg)
        return Result.err(msg)

    required_records = 3
    marked_dates = get_marked_classes(history, "")
    gotten_records = len(marked_dates)

    if gotten_records < required_records:
        msg = f"Cannot record half cohort attendance since the Total Attendance Records: {gotten_records} is less than {required_records}"
        eprint(msg)
        return Result.err(msg)

    # Check if cohort attendance already exists
    cohort_path = get_cohort_path(config, cohort_no)
    if cohort_path.exists():
        print_info(
            f"Cohort Attendance for the Cohort {cohort_no} has already been recorded. This record can be found at the path\nPath: {cohort_path.resolve()}"
        )

        result = input_bool("Do you wish to regenerate this attendance?")
        if result.is_err():
            return result.propagate()

        choice = result.unwrap()
        if not choice:
            return Result.ok(cohort_path)

    # Get all columns and find last class index
    data_cols = pretty.columns
    last_date_idx = data_cols.index(last_class)
    required_cols = data_cols[: last_date_idx + 1]

    # Extract cohort data
    cohort_data = pretty.select(required_cols)

    # Process attendance records
    for column in cohort_data.columns:
        if column in DATA_COLUMNS:
            continue

        # Apply fill_records to each entry in the column
        cohort_data = datamap(cohort_data, column, fill_records, np.str_, pl.String())

    # Output to Excel file
    result = write(cohort_data, cohort_path)
    if result.is_err():
        return result.propagate()

    return Result.ok(cohort_path)
