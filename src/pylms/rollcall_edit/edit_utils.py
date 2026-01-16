from typing import Literal, overload

from ..cli import input_bool
from ..constants import COMMA_DELIM, NAME
from ..data import DataStore
from ..errors import Result, Unit
from ..history import History, all_dates
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

    bad_dates = [date for date in dates if date not in all_dates(history, "")]
    if len(bad_dates) > 0:
        dates_str = COMMA_DELIM.join(bad_dates)
        msg = f"The following dates: '{dates_str}' do not correspond to any class dates"
        raise Result.fail(msg)

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

    pretty = ds.to_pretty()
    data = ds.as_ref()
    idx = serial - 1
    name = pretty.loc[:, NAME].astype(str).iloc[idx]

    print_info(
        f"You are editing the attendance record for {name} with serial no: {serial}"
    )

    if choice:
        date = dates[0]
        record = input_record(history, date, RECORDS)
        if record.is_err():
            return record.propagate()
        record = record.unwrap()

        for date in dates:
            data.at[idx, date] = str(record)

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

        data.at[idx, date] = str(record)
        records.append(record)
        print_info(f"Edited Attendance for {date}")

    print_info(
        f"Attendance record for {name} with serial no: {serial} for dates: '{dates}' edited successfully"
    )
    if kind == "public":
        return Result.unit()
    else:
        return Result.ok(records)


@overload
def edit_single_date(
    ds: DataStore,
    history: History,
    date: str,
    serials: list[int],
    kind: Literal["public"],
) -> Result[Unit]:
    pass


@overload
def edit_single_date(
    ds: DataStore,
    history: History,
    date: str,
    serials: list[int],
    kind: Literal["private"],
) -> Result[RecordStatus] | Result[list[RecordStatus]]:
    pass


def edit_single_date(
    ds: DataStore,
    history: History,
    date: str,
    serials: list[int],
    kind: Literal["private", "public"],
) -> Result[RecordStatus] | Result[list[RecordStatus]] | Result[Unit]:
    if len(serials) == 0:
        raise Result.fail("serials argument cannot be empty")

    if date not in all_dates(history, ""):
        msg = f"Date: '{date}' is not a valid class date"
        raise Result.fail(msg)

    len_rows = ds.as_ref().shape[0]

    bad_serials = [serial for serial in serials if serial < 1 or serial > len_rows]

    if len(bad_serials) > 0:
        serial_text = COMMA_DELIM.join([str(serial) for serial in serials])
        raise Result.fail(
            f"serials specified: '{serial_text}' are invalid. Serials must be between 1 - {len_rows}"
        )

    if len(serials) == 1:
        choice = True
    else:
        choice = input_bool(
            f"Do you wish to make a single edit for every serial in '{serials}'"
        )
        if choice.is_err():
            return choice.propagate()
        choice = choice.unwrap()

    pretty = ds.to_pretty()
    names = pretty.loc[:, NAME].astype(str)
    data = ds.as_ref()

    print_info(f"You are editing the attendance record for date: {date}")

    if choice:
        record = input_record(history, date, RECORDS)
        if record.is_err():
            return record.propagate()
        record = record.unwrap()

        for serial in serials:
            idx = serial - 1
            name = names.iloc[idx]
            data.at[idx, date] = str(record)

            print_info(
                f"Attendance record for {name} with serial no: {serial} for date: '{date}' edited successfully"
            )

        if kind == "public":
            return Result.unit()
        else:
            return Result.ok(record)

    records: list[RecordStatus] = []
    for serial in serials:
        idx = serial - 1
        name = names.iloc[idx]
        record = input_record(history, date, RECORDS)
        if record.is_err():
            return record.propagate()
        record = record.unwrap()

        data.at[idx, date] = str(record)
        records.append(record)

        print_info(
            f"Attendance record for {name} with serial no: {serial} for date: '{date}' edited successfully"
        )

    if kind == "public":
        return Result.unit()
    else:
        return Result.ok(records)
