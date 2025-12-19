import pandas as pd

from ..data import DataStore, DataStream
from ..date import det_week_num
from ..errors import Result, Unit, eprint
from ..models import UpdateFormInfo
from ..paths import ret_update_path
from ..preprocess import clean_new_data
from .add import add


def append_update(
    ds: DataStore, update_stream: DataStream[pd.DataFrame], info: UpdateFormInfo
) -> Result[Unit]:
    week_num: int = det_week_num()
    update_form_path, update_record_path = ret_update_path(info.timestamp)

    if update_record_path.exists():
        msg = f"Entries in the Data Form whose metadata is located at {update_form_path.resolve()} have already been appended."
        eprint(msg)
        return Result.err(msg)

    ds_result: Result[DataStore] = clean_new_data(update_stream)
    if ds_result.is_err():
        msg = f"Error cleaning new data: {ds_result.unwrap_err()}"
        eprint(msg)
        return Result.err(msg)
    ds_to_add: DataStore = ds_result.unwrap()
    new_ds = add(ds, ds_to_add)

    if new_ds.is_err():
        return new_ds.propagate()

    new_ds = new_ds.unwrap()

    print(f"Entries retrieved from the Data Form for Week {week_num} have been saved")
    ds.copy_from(new_ds)
    return Result.unit()
