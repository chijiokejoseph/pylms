import pandas as pd

from pylms.clean_pipeline import clean_new_data
from pylms.data_ops.add import add
from pylms.utils import DataStore, DataStream, date, paths


def append_update(
    ds: DataStore, data_form_stream: DataStream[pd.DataFrame]
) -> DataStore:
    week_num: int = date.det_week_num()
    update_form_path, update_record_path = paths.ret_update_path()

    if update_record_path.exists():
        print(
            f"Entries in the Data Form whose metadata is located at {update_form_path.resolve()} have already been appended."
        )
        return ds

    ds_to_add: DataStore = clean_new_data(data_form_stream)
    ds = add(ds, ds_to_add)
    print(f"Entries retrieved from the Data Form for Week {week_num} have been saved")
    return ds
