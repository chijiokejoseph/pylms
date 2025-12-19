from ..cli import input_option
from ..constants import COMMA_DELIM, WEEK_DAYS
from ..data import DataStore
from ..date import to_unique_week_nums
from ..errors import Result, Unit
from ..history import History, all_dates, save_history, set_class_days, set_cohort
from ..paths import get_paths_weeks
from ..record import RecordStatus


def make_weekly_ds(new_ds: DataStore, dates_list: list[str]) -> None:
    unique_week_nums: list[int] = to_unique_week_nums(dates_list)
    for each_week_num in unique_week_nums:
        new_ds.to_excel(get_paths_weeks() / f"DataStore{each_week_num}.xlsx")
    return None


def input_class_days() -> Result[list[str]]:
    days: list[str] = [""] * 3
    for i in range(3):
        match i:
            case 0:
                title: str = "first"
            case 1:
                title = "second"
            case _:
                title = "third"
        prompt = f"Select {title} class day"
        result = input_option(WEEK_DAYS, prompt=prompt)
        if result.is_err():
            return result.propagate()
        _, class_day = result.unwrap()
        days[i] = class_day
        print(f"\nYou selected {COMMA_DELIM.join(days[slice(None, i + 1)]).strip()}\n")
    days.sort()
    return Result.ok(days)


def normalize(ds: DataStore, history: History) -> Result[Unit]:
    result = input_class_days()
    if result.is_err():
        return result.propagate()

    result = set_class_days(history, result.unwrap(), start=None)
    if result.is_err():
        return result.propagate()

    result = set_cohort(history, ds)
    if result.is_err():
        return result.propagate()

    result = save_history(history)
    if result.is_err():
        return result.propagate()

    date_cols: list[str] = all_dates(history, "")
    ds.as_ref()[date_cols] = RecordStatus.EMPTY
    make_weekly_ds(ds, date_cols)
    return Result.unit()
