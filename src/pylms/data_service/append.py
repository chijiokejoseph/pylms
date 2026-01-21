import pandas as pd

from ..data import DataStore, DataStream
from ..date import det_week_num
from ..errors import Result, Unit
from ..preprocess import clean_new_data
from .add import add


def append_update(
    ds: DataStore, update_stream: DataStream[pd.DataFrame]
) -> Result[Unit]:
    week_num: int = det_week_num()

    add_ds = clean_new_data(update_stream)
    if add_ds.is_err():
        return add_ds.propagate()

    add_ds = add_ds.unwrap()
    new_ds = add(ds, add_ds)

    if new_ds.is_err():
        return new_ds.propagate()

    new_ds = new_ds.unwrap()

    print(f"Entries retrieved from the Data Form for Week {week_num} have been saved")
    ds.copy_from(new_ds)
    return Result.unit()
