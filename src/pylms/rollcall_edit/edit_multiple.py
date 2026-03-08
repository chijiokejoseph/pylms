import polars as pl

from ..cli import input_bool
from ..constants import NAME, SERIAL
from ..data import DataStore
from ..errors import Result, Unit
from ..history import History
from ..info import print_info
from ..query_data import run_query_data
from ..record import RecordStatus
from .edit_utils import edit_single_date, edit_single_serial


def edit_multiple_records(
    ds: DataStore, history: History, dates: list[str]
) -> Result[Unit]:
    data = ds.as_ref()
    pretty = ds.pretty()

    choice = input_bool("Do you wish to make the same edit for all selected students")

    if choice.is_err():
        return choice.propagate()
    choice = choice.unwrap()

    if choice:
        serials = run_query_data(ds)
        if serials.is_err():
            return serials.propagate()
        serials = serials.unwrap()

        names = pretty[NAME]

        first_name = names.item(0)
        print_info(
            f"You will make edit for the first selection: {first_name} and this same edit will be used for all"
        )
        serial = serials[0]
        record = edit_single_serial(ds, history, serial, dates, "private")
        if record.is_err():
            return record.propagate()
        record = record.unwrap()

        if isinstance(record, RecordStatus):
            data = data.with_columns(
                [
                    pl.when(pl.col(SERIAL).is_in(serials))
                    .then(pl.lit(str(record)))
                    .otherwise(pl.col(date))
                    .alias(date)
                    for date in dates
                ]
            )
            for serial in serials:
                idx = serial - 1
                name: str = names.item(idx)
                print_info(
                    f"Attendance record for {name} with serial: '{serial}' for dates: '{dates}' has been edited successfully"
                )
        else:
            for serial in serials:
                data = data.with_columns(
                    [
                        pl.when(pl.col(SERIAL) == serial)
                        .then(pl.lit(str(each_record)))
                        .otherwise(pl.col(date))
                        .alias(date)
                        for each_record, date in zip(record, dates)
                    ]
                )
                name = names.item(serial - 1)
                print_info(
                    f"Attendance record for {name} with serial: '{serial}' for dates: '{dates}' has been edited successfully"
                )

        result = ds.copy_from(data)
        if result.is_err():
            return result.propagate()

        return Result.unit()

    for date in dates:
        serials = run_query_data(ds)
        if serials.is_err():
            return serials.propagate()
        serials = serials.unwrap()

        result = edit_single_date(ds, history, date, serials, "public")
        if result.is_err():
            return result.propagate()

    return Result.unit()
