from datetime import datetime
from pathlib import Path

import pandas as pd

from ..cli import input_bool
from ..constants import COHORT, DATA_COLUMNS, DATE_FMT
from ..data import DataStore, DataStream
from ..errors import Result, eprint
from ..history import (
    History,
    get_available_cds_forms,
    get_marked_classes,
    retrieve_dates,
)
from ..info import print_info
from ..models import CDSFormInfo
from ..paths import get_cohort_path
from ..record import RecordStatus


# return a more appropriate output for use by the NCAIR team that
# scrutinize the half-cohort attendance
def fill_norm_records(record_input: str) -> RecordStatus:
    if record_input in [
        RecordStatus.CDS,
        RecordStatus.EXCUSED,
        RecordStatus.PRESENT,
    ]:
        return RecordStatus.PRESENT
    else:
        return RecordStatus.ABSENT


def fill_records(record_input: str) -> RecordStatus:
    match str(record_input):
        case RecordStatus.PRESENT:
            return RecordStatus.PRESENT
        case RecordStatus.EXCUSED:
            return RecordStatus.EXCUSED
        case RecordStatus.CDS:
            return RecordStatus.CDS
        case RecordStatus.NO_CLASS:
            return RecordStatus.NO_CLASS
        case _:
            return RecordStatus.ABSENT


def record_cohort(ds: DataStore, history: History) -> Result[Path]:
    # get DataStore data in its pretty form
    pretty_data: pd.DataFrame = ds.pretty()

    # get cohort no
    cohort_no: int = pretty_data[COHORT].astype(int).iloc[0]

    # get class dates
    dates = retrieve_dates("")
    if dates.is_err():
        return dates.propagate()

    dates = dates.unwrap()

    today: datetime = datetime.now()
    past_classes: list[str] = [
        each_date
        for each_date in dates
        if datetime.strptime(each_date, DATE_FMT) <= today
    ]
    last_class: str = past_classes[-1]

    # check that the CDS days of the NYSC students in the cohort
    # have been recorded before taking cohort attendance
    # this is done by checking that at least one cds form has been generated and retrieved
    # and that there are no cds forms unretrieved.
    available_cds_forms: list[CDSFormInfo] = get_available_cds_forms(history)
    if len(available_cds_forms) != 0 and len(history.recorded_cds_forms) > 0:
        msg = "Cannot record half cohort attendance since the CDS days of the NYSC students has not yet been recorded. Please record the CDS days then try again."
        print_info(msg)
        return Result.err(msg)

    required_records: int = 3
    marked_dates = get_marked_classes(history, "")
    gotten_records = len(marked_dates)

    if gotten_records < required_records:
        msg = f"Cannot record half cohort attendance since the Total Attendance Records: {gotten_records} is less than {required_records}"
        eprint(msg)
        return Result.err(msg)

    # if the half-cohort attendance has already been generated, return early
    cohort_path: Path = get_cohort_path(cohort_no)
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

    # get all the columns in the data
    data_cols: list[str] = pretty_data.columns.tolist()

    # get the index of the column that corresponds to the `last_class_date` of the half-cohort week
    last_date_idx: int = data_cols.index(last_class)

    # extract all the columns from the beginning of the dataset to the `last_class_date` column
    required_cols: list[str] = data_cols[: last_date_idx + 1]

    # extract the entries for the half-cohort attendance
    cohort_data: pd.DataFrame = pretty_data.loc[:, required_cols]

    _ = fill_norm_records("Excused")
    for column in cohort_data.columns.tolist():
        # if `column` is in `DATA_COLUMNS` i.e., it is not a date column skip
        if column in DATA_COLUMNS:
            continue
        # format column by using fill_record on all its entries
        class_record: list[str] = cohort_data[column].tolist()
        new_class_record = [fill_records(record) for record in class_record]
        # update the column data with the `new_class_record`
        cohort_data[column] = new_class_record

    # output the data to local file storage
    cohort_stream: DataStream[pd.DataFrame] = DataStream(cohort_data)

    result = cohort_stream.to_excel(cohort_path)
    if result.is_err():
        return result.propagate()

    return Result.ok(cohort_path)
