from pylms.errors import Result
from pylms.utils import DataStore, date, paths
from pylms.history import History
from pylms.record import RecordStatus
from pylms.constants import WEEK_DAYS, COMMA_DELIM
from pylms.cli import input_option


def make_weekly_ds(new_ds: DataStore, dates_list: list[str]) -> None:
    unique_week_nums: list[int] = date.to_unique_week_nums(dates_list)
    for each_week_num in unique_week_nums:
        new_ds.to_excel(paths.get_paths_weeks() / f"DataStore{each_week_num}.xlsx")
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
            return Result[list[str]].err(result.unwrap_err())
        _, class_day = result.unwrap()
        days[i] = class_day
        print(f"\nYou selected {COMMA_DELIM.join(days[slice(None, i + 1)]).strip()}\n")
    days.sort()
    return Result[list[str]].ok(days)


def normalize(ds: DataStore, history: History) -> None:
    result = input_class_days()
    if result.is_err():
        return
    history.set_class_days(result.unwrap(), start=None)
    history.set_cohort(ds)
    history.save()
    date_cols: list[str] = history.str_dates()
    ds.as_ref()[date_cols] = RecordStatus.EMPTY
    make_weekly_ds(ds, date_cols)
