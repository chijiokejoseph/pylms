import pandas as pd

from pylms.errors import Result
from pylms.preprocess import clean_new_data
from pylms.data_ops.add import add
from pylms.utils import DataStore, DataStream, date, paths
from pylms.models import UpdateFormInfo

def append_update(
    ds: DataStore, update_stream: DataStream[pd.DataFrame], info: UpdateFormInfo
) -> None:
    week_num: int = date.det_week_num()
    update_form_path, update_record_path = paths.ret_update_path(info.timestamp)

    if update_record_path.exists():
        print(
            f"Entries in the Data Form whose metadata is located at {update_form_path.resolve()} have already been appended."
        )
        return None

    ds_result: Result[DataStore] = clean_new_data(update_stream)
    if ds_result.is_err():
        print(f"Error cleaning new data: {ds_result.unwrap_err()}")
        return None
    ds_to_add: DataStore = ds_result.unwrap()
    new_ds: DataStore = add(ds, ds_to_add)
    print(f"Entries retrieved from the Data Form for Week {week_num} have been saved")
    ds.copy_from(new_ds)
    return None
