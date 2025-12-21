from ..cli import input_option
from ..constants import COMMA_DELIM, WEEK_DAYS
from ..data import DataStore
from ..date import to_unique_week_nums
from ..errors import Result, Unit
from ..history import History, all_dates, save_history, set_class_days, set_cohort
from ..paths import get_paths_weeks
from ..record import RecordStatus


def make_weekly_ds(new_ds: DataStore, dates_list: list[str]) -> None:
    """Write weekly DataStore files for unique week numbers.

    Given a DataStore and a list of date strings, compute the unique week
    numbers using `to_unique_week_nums` and write the DataStore to an Excel
    file for each unique week number. Filenames are produced using the
    `get_paths_weeks()` base path and have the format `DataStore{week}.xlsx`.

    Args:
        new_ds (DataStore): DataStore instance to be written to disk.
        dates_list (list[str]): List of date strings from which week numbers
            will be derived.

    Returns:
        None
    """
    unique_week_nums: list[int] = to_unique_week_nums(dates_list)
    for each_week_num in unique_week_nums:
        new_ds.to_excel(get_paths_weeks() / f"DataStore{each_week_num}.xlsx")
    return None


def input_class_days() -> Result[list[str]]:
    """Interactively prompt the user to select three class days.

    Prompts the user three times to select a class day (first, second,
    third) from the `WEEK_DAYS` options using `input_option`. After each
    selection the current selections are printed. The returned list of days
    is sorted before being returned inside `Result.ok`.

    Returns:
        Result[list[str]]: Ok result with a sorted list of three selected
            class day strings, or an error `Result` propagated from the
            interactive prompt when selection fails.
    """
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
    """Normalize stateful settings and prepare weekly data files.

    Orchestrates a sequence of interactive and persistence operations used to
    normalize scheduling/state information for the provided `DataStore` and
    `History` objects:

    1. Prompt the user for class days via `input_class_days`.
    2. Persist the selected class days to the `history` with `set_class_days`.
    3. Associate a cohort with the `DataStore` via `set_cohort`.
    4. Save the updated history using `save_history`.
    5. Compute date columns from history, mark them as empty in the `DataStore`
       and write weekly DataStore files via `make_weekly_ds`.

    Each step propagates any error `Result` returned by the underlying calls.

    Args:
        ds (DataStore): The DataStore to prepare and write weekly files for.
        history (History): History object to update with class days and cohort.

    Returns:
        Result[Unit]: Ok result when all operations succeed, or an error
            `Result` propagated from the first failing operation.
    """
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
