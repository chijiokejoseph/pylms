from typing import Literal, overload

from ..cli import input_bool, provide_serials
from ..constants import NAME
from ..data import DataStore
from ..errors import Result, Unit, eprint
from ..history import History, get_marked_classes
from ..info import print_info
from ..record import RecordStatus
from .record_input import RECORDS, input_record


@overload
def edit_single_serial(
    ds: DataStore,
    history: History,
    serial: int,
    dates: list[str],
    kind: Literal["private"],
) -> Result[RecordStatus] | Result[list[RecordStatus]]:
    pass


@overload
def edit_single_serial(
    ds: DataStore,
    history: History,
    serial: int,
    dates: list[str],
    kind: Literal["public"],
) -> Result[Unit]:
    pass


def edit_single_serial(
    ds: DataStore,
    history: History,
    serial: int,
    dates: list[str],
    kind: Literal["private", "public"],
) -> Result[RecordStatus] | Result[list[RecordStatus]] | Result[Unit]:
    if len(dates) == 0:
        raise Result.fail("dates argument cannot be empty")

    len_rows = ds.as_ref().shape[0]

    if serial < 1 or serial > len_rows:
        raise Result.fail(f"serial argument must be between 1 - {len_rows}")

    if len(dates) == 1:
        choice = True
    else:
        choice = input_bool(
            f"Do you wish to make a single edit for every date in '{dates}'"
        )
        if choice.is_err():
            return choice.propagate()
        choice = choice.unwrap()

    names = ds.to_pretty()
    data = ds.as_ref()
    idx = serial - 1
    name = names[NAME].astype(str).iloc[idx]

    print_info(
        f"You are editing the attendance record for {name} with serial no: {serial}"
    )

    marked_dates = get_marked_classes(history, "")
    diff = set(dates).difference(set(marked_dates))
    if len(diff) > 0:
        bad_dates = list(diff)
        bad_dates.sort()
        msg = f"Dates '{bad_dates}' in dates argument '{dates} have not been marked. Please mark those dates and try again"
        eprint(msg)
        raise Result.fail(msg)

    if choice:
        date = dates[0]
        record = input_record(history, date, RECORDS)
        if record.is_err():
            return record.propagate()
        record = record.unwrap()

        for date in dates:
            data.loc[idx, date] = record

        print_info(
            f"Attendance record for {name} with serial no: {serial} for dates: '{dates}' edited successfully"
        )
        if kind == "public":
            return Result.unit()
        else:
            return Result.ok(record)

    records: list[RecordStatus] = []
    for date in dates:
        record = input_record(history, date, RECORDS)
        if record.is_err():
            return record.propagate()
        record = record.unwrap()
        data.loc[idx, date] = record
        records.append(record)
        print_info(f"Edited Attendance for {date}")

    print_info(
        f"Attendance record for {name} with serial no: {serial} for dates: '{dates}' edited successfully"
    )
    if kind == "public":
        return Result.unit()
    else:
        return Result.ok(records)


def edit_single_record(
    ds: DataStore, history: History, dates: list[str]
) -> Result[Unit]:
    serials = provide_serials(ds)
    if serials.is_err():
        return serials.propagate()
    serials = serials.unwrap()

    if len(serials) > 1:
        msg = "This edit feature allows for editing the attendance of only a single student, yet multiple student serials have been provided"
        eprint(msg)
        return Result.err(msg)

    serial = serials[0]

    return edit_single_serial(ds, history, serial, dates, "public")
