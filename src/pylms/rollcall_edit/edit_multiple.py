from ..cli import input_bool, provide_serials
from ..constants import NAME
from ..data import DataStore
from ..errors import Result, Unit
from ..history import History
from ..info import print_info
from ..record import RecordStatus
from .edit_utils import edit_single_date, edit_single_serial


def edit_multiple_records(
    ds: DataStore, history: History, dates: list[str]
) -> Result[Unit]:
    data = ds.as_ref()
    pretty = ds.to_pretty()

    choice = input_bool("Do you wish to make the same edit for all selected students")

    if choice.is_err():
        return choice.propagate()
    choice = choice.unwrap()

    if choice:
        serials = provide_serials(ds)
        if serials.is_err():
            return serials.propagate()
        serials = serials.unwrap()

        idxs = [serial - 1 for serial in serials]
        names = pretty.loc[:, NAME].astype(str)

        first_name = names.iloc[0]
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
                    data.at[idx, date] = str(record)
                name = names.iloc[idx]
                print_info(
                    f"Attendance record for {name} with serial: '{idx + 1}' for dates: '{dates}' has been edited successfully"
                )
        else:
            for idx in rest:
                for each_record, date in zip(record, dates):
                    data.at[idx, date] = str(each_record)
                name = names.iloc[idx]
                print_info(
                    f"Attendance record for {name} with serial: '{idx + 1}' for dates: '{dates}' has been edited successfully"
                )

        return Result.unit()

    for date in dates:
        serials = provide_serials(ds)
        if serials.is_err():
            return serials.propagate()
        serials = serials.unwrap()

        result = edit_single_date(ds, history, date, serials, "public")
        if result.is_err():
            return result.propagate()

    return Result.unit()
