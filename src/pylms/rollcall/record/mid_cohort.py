from datetime import datetime
from pathlib import Path

import pandas as pd

from pylms.constants import COHORT, DATA_COLUMNS, DATE_FMT
from pylms.record import RecordStatus
from pylms.utils import DataStore, DataStream, date, paths


def record_mid_cohort(ds: DataStore) -> Path | None:
    # get DataStore data in its pretty form
    pretty_data: pd.DataFrame = ds.pretty()

    # get cohort no
    cohort_no: int = pretty_data[COHORT].iloc[0]

    # get class dates
    dates_list: list[str] = date.retrieve_dates()

    today: datetime = datetime.now()
    past_class_dates: list[str] = [
        each_date
        for each_date in dates_list
        if datetime.strptime(each_date, DATE_FMT) <= today
    ]
    last_class_date: str = past_class_dates[-1]

    cds_record: Path = paths.get_cds_path("record")
    # check that the CDS days of the NYSC students in the cohort have been recorded before taking half-cohort attendance
    if not cds_record.exists():
        print(
            "Cannot record half cohort attendance since the CDS days of the NYSC students has not yet been recorded. Please record the CDS days then try again."
        )

    required_records: int = 3
    gotten_records: int = 0
    for class_date in past_class_dates:
        class_idx: int = dates_list.index(class_date)
        class_num: int = class_idx + 1
        class_record_file: Path = paths.get_class_path(class_date, "record")
        # check that every previous class date has had its attendance recorded.
        if class_record_file.exists():
            gotten_records += 1
        else:
            print(f"\nRecord for Class {class_num} on date {class_date} is missing")

    if gotten_records < required_records:
        print(
            f"Cannot record half cohort attendance since the Total Attendance Records is less than {required_records}"
        )
        return None

    # if the half-cohort attendance has already been generated, return early
    half_cohort_path: Path = paths.get_cohort_path(cohort_no)
    if half_cohort_path.exists():
        print(
            f"Half Cohort Attendance for the Cohort {cohort_no} already recorded. This record can be found at the path:  \n{half_cohort_path.resolve()}"
        )
        return None

    # get all the columns in the data
    data_cols: list[str] = pretty_data.columns.tolist()

    # get the index of the column that corresponds to the `last_class_date` of the half-cohort week
    last_date_idx: int = data_cols.index(last_class_date)

    # extract all the columns from the beginning of the dataset to the `last_class_date` column
    required_cols: list[str] = data_cols[: last_date_idx + 1]

    # extract the entries for the half-cohort attendance
    half_cohort_data: pd.DataFrame = pretty_data.loc[:, required_cols]

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

    _ = fill_norm_records("Excused")
    for column in half_cohort_data.columns.tolist():
        # if `column` is in `DATA_COLUMNS` i.e., it is not a date column skip
        if column in DATA_COLUMNS:
            continue
        # format column by using fill_record on all its entries
        class_record: list[str] = half_cohort_data[column].tolist()
        new_class_record = [fill_records(record) for record in class_record]
        # update the column data with the `new_class_record`
        half_cohort_data[column] = new_class_record

    # output the data to local file storage
    half_cohort_stream: DataStream[pd.DataFrame] = DataStream(half_cohort_data)
    half_cohort_stream.to_excel(half_cohort_path)
    return half_cohort_path
