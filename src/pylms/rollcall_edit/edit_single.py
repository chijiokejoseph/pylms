from ..cli import provide_serials
from ..data import DataStore
from ..errors import Result, Unit, eprint
from ..history import History
from .edit_utils import edit_single_serial


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
