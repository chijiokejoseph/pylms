import polars as pl

from ..cli import input_bool
from ..data import DataStore
from ..errors import Result, Unit, eprint
from ..history import (
    History,
    add_held_class,
    add_marked_class,
    get_unheld_classes,
    get_unmarked_classes,
)
from ..info import printpass
from ..record import RecordStatus
from .record_input import input_record


def multi_input_record(
    history: History, dates: list[str]
) -> Result[list[RecordStatus]]:
    dates_str = ", ".join(dates)

    if len(dates) == 1:
        choice = True
    else:
        result = input_bool(f"Are you making the same edit for dates: {dates_str}")
        if result.is_err():
            return result.propagate()

        choice = result.unwrap()

    if choice:
        first_date = dates[0]
        record = input_record(
            history,
            first_date,
            [RecordStatus.PRESENT, RecordStatus.ABSENT, RecordStatus.NO_CLASS],
        )
        if record.is_err():
            return record.propagate()
        record = record.unwrap()
        return Result.ok([record])

    records: list[RecordStatus] = []
    for each_date in dates:
        result = input_record(
            history,
            each_date,
            [RecordStatus.PRESENT, RecordStatus.ABSENT, RecordStatus.NO_CLASS],
        )
        if result.is_err():
            return result.propagate()
        record = result.unwrap()
        records.append(record)

    return Result.ok(records)


def return_expr(record: RecordStatus, date: str) -> pl.Expr:
    return (  # if new record is NO_CLASS
        pl.when(record == RecordStatus.NO_CLASS)
        # return NO_CLASS
        .then(pl.lit(str(RecordStatus.NO_CLASS)))
        .otherwise(
            # if existing record is CDS
            pl.when(pl.col(date) == str(RecordStatus.CDS))
            # return CDS
            .then(pl.lit(str(RecordStatus.CDS)))
            .otherwise(
                # if existing record is EXCUSED and new is ABSENT
                pl.when(
                    (pl.col(date) == str(RecordStatus.EXCUSED))
                    & (record == RecordStatus.ABSENT)
                )
                # return EXCUSED
                .then(pl.lit(str(RecordStatus.EXCUSED)))
                # else return new record
                .otherwise(pl.lit(str(record)))
            )
        )
        .alias(date)
    )


def edit_all_records(
    ds: DataStore, history: History, dates_to_mark: list[str]
) -> Result[Unit]:
    if len(dates_to_mark) == 0:
        msg = "dates_to_mark should not be empty"
        eprint(msg)
        return Result.err(msg)

    records = multi_input_record(history, dates_to_mark)
    if records.is_err():
        return records.propagate()

    records = records.unwrap()

    data_ref = ds.as_ref()
    if len(records) == 1:
        record = records[0]
        data_ref = data_ref.with_columns(
            [return_expr(record, date) for date in dates_to_mark]
        )
    else:
        for record, date in zip(records, dates_to_mark):
            data_ref = data_ref.with_columns(return_expr(record, date))

    ds.copy_from(data_ref)
    unheld_dates = get_unheld_classes(history, "")
    for date in dates_to_mark:
        if date not in unheld_dates:
            continue
        result = add_held_class(history, date)
        if result.is_err():
            return result.propagate()
        printpass(f"Recorded that Class held on '{date}'")

    unmarked_dates = get_unmarked_classes(history, "")
    for date in dates_to_mark:
        if date not in unmarked_dates:
            continue
        result = add_marked_class(history, date)
        if result.is_err():
            return result.propagate()
        printpass(f"Recorded that Class marked on '{date}'")

    return Result.unit()
