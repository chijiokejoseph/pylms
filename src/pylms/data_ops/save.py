from pathlib import Path

from pylms.utils import DataStore, date, paths


def save(ds: DataStore) -> None:
    week_num: int = date.det_week_num()
    # get all week nums for this cohort
    week_nums: list[int] = date.to_unique_week_nums(date.retrieve_dates())
    # get all the week nums that are greater than the current week num but still in this cohort
    new_week_nums: list[int] = [num for num in week_nums if num >= week_num]
    if len(new_week_nums) == 0:
        new_week_nums = [week_nums[-1]]
    DataStore_names_display: str = ""
    # for each new week num, write the new data in `ds` to its corresponding path.
    for num in new_week_nums:
        new_week_ds_path: Path = paths.get_paths_weeks() / f"DataStore{num}.xlsx"
        DataStore_names_display += f"DataStore{num}.xlsx, "
        ds.to_excel(new_week_ds_path)
    general_week_ds_path: Path = paths.get_paths_excel()["DataStore"]
    ds.to_excel(general_week_ds_path)

    DataStore_names_display = DataStore_names_display.strip().removesuffix(",")
    print(f"Save made to the following files: {DataStore_names_display}")
