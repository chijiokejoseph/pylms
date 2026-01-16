import pandas as pd

from ..cli import input_bool
from ..data import DataStore
from ..errors import Result, Unit, eprint
from ..history import (
    History,
    add_held_class,
    add_marked_class,
    get_unmarked_classes,
    match_date_index,
)
from ..info import print_info, printpass
from ..record import RecordStatus, retrieve_record
from .record_input import input_record


def _edit_record(ds: DataStore, history: History, each_date: str) -> Result[Unit]:
    record = input_record(
        history,
        each_date,
        [RecordStatus.PRESENT, RecordStatus.ABSENT, RecordStatus.NO_CLASS],
    )
    if record.is_err():
        return record.propagate()
    selected_record: RecordStatus = record.unwrap()

    data_ref: pd.DataFrame = ds.as_ref()
    records = data_ref[each_date].astype(str).tolist()
    class_record = [retrieve_record(record) for record in records]
    new_class_record = [
        str(_fill(old_record, selected_record)) for old_record in class_record
    ]
    data_ref[each_date] = data_ref[each_date].astype(str)
    data_ref[each_date] = new_class_record
    return Result.unit()


def _fill(existing_record: RecordStatus, fill_record: RecordStatus) -> RecordStatus:
    # If no class is held that day return no class
    if fill_record == RecordStatus.NO_CLASS:
        return fill_record

    # If the student's record indicates that that day is his CDS, then prefer the CDS record
    if existing_record == RecordStatus.CDS:
        return existing_record

    # If all the students are marked absent but a student is marked excused, prefer his excused record
    if fill_record == RecordStatus.ABSENT and existing_record == RecordStatus.EXCUSED:
        return existing_record

    # Else unequivocally return the fill record set by the user.
    return fill_record


def edit_all_records(
    ds: DataStore, history: History, dates_to_mark: list[str]
) -> Result[Unit]:
    if len(dates_to_mark) == 0:
        msg = "dates_to_mark should not be empty"
        eprint(msg)
        return Result.err(msg)

    dates_str = ", ".join(dates_to_mark)

    if len(dates_to_mark) == 1:
        choice = True
    else:
        result = input_bool(f"Are you making the same edit for dates: {dates_str}")
        if result.is_err():
            return result.propagate()

        choice = result.unwrap()

    if choice:
        first_date = dates_to_mark[0]
        print_info(
            f"Enter the record for the first date: '{first_date}' and it will be used for all specified dates."
        )
        result = _edit_record(ds, history, first_date)
        if result.is_err():
            return result.propagate()
    else:
        for each_date in dates_to_mark:
            result = _edit_record(ds, history, each_date)
            if result.is_err():
                return result.propagate()

    unmarked_dates = get_unmarked_classes(history, "")
    edited_dates = [date for date in dates_to_mark if date in unmarked_dates]

    for date in edited_dates:
        result = add_held_class(history, date)
        if result.is_err():
            return result.propagate()

        result = add_marked_class(history, date)
        if result.is_err():
            return result.propagate()

        class_num = match_date_index(history, date).unwrap()
        printpass(f"Recorded attendance for Class {class_num} held on '{date}'")

    return Result.unit()
