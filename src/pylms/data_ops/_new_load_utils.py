from pylms.cli import input_str
from pylms.utils import DataStore, date, paths
from pylms.data_ops.data_status import DataStatus
from pylms.clean_pipeline import clean_reg_data
from pathlib import Path
import sys


def _load_ds() -> tuple[DataStore, DataStatus]:
    path: Path = paths.get_paths_excel()["DataStore"]
    if path.exists():
        init_ds: DataStore = DataStore.from_local(path)
        return init_ds, DataStatus.OLD

    print("DataStore not found. Program will try to create DataStore from scratch. ")
    response: str = input_str("Should I continue: [y/N]: ", lambda x: True)
    if response.lower().strip() in ["y", "yes"]:
        init_ds = clean_reg_data()
        print("Preprocessing operation completed successfully.\n")
        return init_ds, DataStatus.NEW
    else:
        sys.exit(
            "😔 Sorry to let you down friend. \nPlease rerun the program and preprocess a new registration data before continuing with any other operations. \nThank you for visiting today."
        )


def _load_dates(ds: DataStore) -> list[str]:
    if not paths.get_paths_json()["Date"].exists():
        date.prepare_dates(ds)
    return date.retrieve_dates()


def _make_weekly_ds(new_ds: DataStore) -> None:
    dates_list: list[str] = _load_dates(new_ds)
    unique_week_nums: list[int] = date.to_unique_week_nums(dates_list)
    for each_week_num in unique_week_nums:
        new_ds.to_excel(paths.get_paths_weeks() / f"DataStore{each_week_num}.xlsx")
    return None
