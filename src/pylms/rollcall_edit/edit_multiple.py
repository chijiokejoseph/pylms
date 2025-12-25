from pylms.cli import input_bool, provide_serials
from pylms.constants import NAME
from pylms.data import DataStore
from pylms.errors import Result, Unit
from pylms.history import History
from pylms.info import print_info
from pylms.record import RecordStatus
from pylms.rollcall_edit.edit_single import edit_single_serial


def edit_multiple_records(
    ds: DataStore, history: History, dates: list[str]
) -> Result[Unit]:
    data = ds.as_ref()
    names = ds.to_pretty()

    serials = provide_serials(ds)
    if serials.is_err():
        return serials.propagate()
    serials = serials.unwrap()

    idxs = [serial - 1 for serial in serials]
    names = [names[NAME].astype(str).iloc[idx] for idx in idxs]

    choice = input_bool(
        f"Do you wish to make the same edit for all selected students '{names}'"
    )
    if choice.is_err():
        return choice.propagate()
    choice = choice.unwrap()

    if choice:
        first_name = names[0]
        print_info(
            f"You will make edit for the first selection: {first_name} and this same edit will be used for all"
        )
        serial = serials[0]
        record = edit_single_serial(ds, history, serial, dates, "private")
        if record.is_err():
            return record.propagate()
        record = record.unwrap()

        rest = idxs[1:]
        if isinstance(record, RecordStatus):
            for idx in rest:
                for date in dates:
                    data.loc[idx, date] = record
        else:
            for each_record, date in zip(record, dates):
                for idx in rest:
                    data.loc[idx, date] = each_record

    for serial in serials:
        result = edit_single_serial(ds, history, serial, dates, "public")
        if result.is_err():
            return result.propagate()

    return Result.unit()
