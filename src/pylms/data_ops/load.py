import sys
from pathlib import Path

from pylms.data_ops._new_load_utils import _load_ds, _make_weekly_ds
from pylms.data_ops.data_status import DataStatus
from pylms.utils import DataStore, date, paths


def load() -> DataStore:
    init_ds, status = _load_ds()
    if status == DataStatus.NEW:
        _make_weekly_ds(init_ds)
        return init_ds

    today_week_num: int = date.det_week_num()
    dates_list: list[str] = date.retrieve_dates()
    unique_week_nums: tuple[int, ...] = date.to_unique_week_nums(dates_list)
    last_week_num: int = unique_week_nums[-1]
    if today_week_num > last_week_num:
        print(
            f"The cohort period for which the DataStore was first created has ended. Returning the last recorded DataStore i.e., DataStore{last_week_num}.xlsx"
        )
        today_week_num = last_week_num
    week_ds_path: Path = paths.get_paths_weeks() / f"DataStore{today_week_num}.xlsx"
    if not week_ds_path.exists():
        msg: str = f"""
Existing Preprocessed DataStore found, but no record of the DataStore `DataStore{today_week_num}.xlsx
The DataStore for this week used for handling updates and changes to data. 

Please check the following directories for corruption: 
    i. `data`
    ii. `data/weeks`
    
The week num of this program run is {today_week_num} and the DataStore to be accessed for this week is
DataStore{today_week_num}.xlsx which has not been found.

What to do? 
    i. Inspect that DataStore{today_week_num}.xlsx is not missing from its directory `data/weeks`
    
If missing?
There are two solutions: 
    i. If missing and there are no minimal differences between it and the original
    copy `DataStore.xlsx` stored directly in `data` folder to the location `data/weeks` 
    and rename the file to `DataStore{today_week_num}.xlsx
    ii. Delete the data `DataStore.xlsx` directly stored in `data` 
    and the json file `dates.json` stored in `data/json` 
    and re-preprocess the entire original data from scratch  
            """
        sys.exit(msg)
    else:
        week_ds: DataStore = DataStore.from_local(week_ds_path)
        return week_ds
