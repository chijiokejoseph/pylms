from ..data import DataStore, DataStream
from ..errors import Result, Unit
from ..info import print_info
from ..models import UpdateFormInfo
from ..preprocess import clean_new_data
from .add import add


def append_update(
    ds: DataStore, update_stream: DataStream, info: UpdateFormInfo
) -> Result[Unit]:
    week_num = info.week_num

    new_ds = clean_new_data(update_stream)
    if new_ds.is_err():
        return new_ds.propagate()

    new_ds = new_ds.unwrap()
    new_ds = add(new_ds, new_ds)

    if new_ds.is_err():
        return new_ds.propagate()

    new_ds = new_ds.unwrap()

    print_info(
        f"Entries retrieved from the Data Form for Week {week_num} have been saved"
    )
    return ds.copy_from(new_ds)
