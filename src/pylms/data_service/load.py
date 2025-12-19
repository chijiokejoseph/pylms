from pathlib import Path

from ..data import DataStore
from ..date import det_week_num, to_unique_week_nums
from ..errors import Result
from ..history import retrieve_dates
from ..info import print_info
from ..paths import get_paths_excel, get_paths_weeks
from .prefill import prefill_ds


def load() -> Result[DataStore]:
    # get DataStore path
    path: Path = get_paths_excel()["DataStore"]

    # load DataStore from path if it exists
    # else return dummy DataStore
    if path.exists():
        init_ds = DataStore.from_local(path)
        if init_ds.is_err():
            return init_ds.propagate()

        init_ds = init_ds.unwrap()
    else:
        msg = "DataStore not found. Please register a new cohort first before performing any other operations."
        print_info(msg)
        return Result.ok(prefill_ds())

    # get today's week number
    today_week_num: int = det_week_num()

    # get all class dates for this cohort
    dates_list = retrieve_dates("")
    if dates_list.is_err():
        return dates_list.propagate()

    dates_list = dates_list.unwrap()

    # get all unique week numbers for this cohort
    unique_week_nums: list[int] = to_unique_week_nums(dates_list)

    # get the last week number for this cohort
    last_week_num: int = unique_week_nums[-1]

    # check if the cohort period for which the DataStore was first created has ended
    if today_week_num > last_week_num:
        print_info(
            f"The cohort period for which the DataStore was first created has ended. Returning the last recorded DataStore i.e., DataStore{last_week_num}.xlsx\n"
        )
        today_week_num = last_week_num

    # get the DataStore for the week corresponding to today's week number
    week_ds_path: Path = get_paths_weeks() / f"DataStore{today_week_num}.xlsx"

    # load DataStore for the week corresponding to today's week number
    # else return the current DataStore
    if not week_ds_path.exists():
        return Result.ok(init_ds)
    else:
        week_ds = DataStore.from_local(week_ds_path)
        return week_ds
