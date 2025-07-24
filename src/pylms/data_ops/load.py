from pathlib import Path

from pylms.data_ops.prefill import prefill_ds
from pylms.utils import DataStore, date, paths


def load() -> DataStore:
    # get DataStore path
    path: Path = paths.get_paths_excel()["DataStore"]

    # load DataStore from path if it exists
    # else return dummy DataStore
    if path.exists():
        init_ds = DataStore.from_local(path)
    else:
        print(
            "DataStore not found. Please register a new cohort first before performing any other operations."
        )
        return prefill_ds()

    # get today's week number
    today_week_num: int = date.det_week_num()
    
    # get all class dates for this cohort
    dates_list: list[str] = date.retrieve_dates()
    
    # get all unique week numbers for this cohort
    unique_week_nums: list[int] = date.to_unique_week_nums(dates_list)
    
    # get the last week number for this cohort
    last_week_num: int = unique_week_nums[-1]
    
    # check if the cohort period for which the DataStore was first created has ended
    if today_week_num > last_week_num:
        print(
            f"The cohort period for which the DataStore was first created has ended. Returning the last recorded DataStore i.e., DataStore{last_week_num}.xlsx\n"
        )
        today_week_num = last_week_num

    # get the DataStore for the week corresponding to today's week number
    week_ds_path: Path = paths.get_paths_weeks() / f"DataStore{today_week_num}.xlsx"

    # load DataStore for the week corresponding to today's week number
    # else return the current DataStore
    if not week_ds_path.exists():
        return init_ds
    else:
        week_ds: DataStore = DataStore.from_local(week_ds_path)
        return week_ds
