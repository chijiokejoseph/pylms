from pathlib import Path

from ..data import DataStore
from ..date import det_week_num, to_unique_week_nums
from ..errors import Result, Unit, eprint
from ..history import retrieve_dates
from ..info import printpass
from ..paths import get_paths_excel, get_paths_weeks


def save(ds: DataStore) -> Result[Unit]:
    if ds.prefilled:
        msg = "Error: DataStore is prefilled and has no actual data"
        eprint(msg)
        return Result.err(msg)
    week_num: int = det_week_num()

    # get all week nums for this cohort
    dates = retrieve_dates("")
    if dates.is_err():
        return dates.propagate()

    dates = dates.unwrap()
    week_nums: list[int] = to_unique_week_nums(dates)

    # get all the week nums that are greater than the current week num but still in this cohort
    new_week_nums: list[int] = [num for num in week_nums if num >= week_num]
    if len(new_week_nums) == 0:
        new_week_nums = [week_nums[-1]]
    DataStore_names_display: str = ""

    # for each new week num, write the new data in `ds` to its corresponding path.
    for num in new_week_nums:
        new_week_ds_path: Path = get_paths_weeks() / f"DataStore{num}.xlsx"
        DataStore_names_display += f"DataStore{num}.xlsx, "
        ds.to_excel(new_week_ds_path)
    general_week_ds_path: Path = get_paths_excel()["DataStore"]
    ds.to_excel(general_week_ds_path)

    DataStore_names_display = DataStore_names_display.strip().removesuffix(",")
    printpass(f"Save made to the following files: {DataStore_names_display}")
    return Result.unit()
