from pylms.utils import DataStore
from pylms.history import History
from pylms.record import RecordStatus
from pylms.constants import WEEK_DAYS
from pylms.cli import input_option


def input_class_days() -> list[str]:
    days: list[str] = [""] * 3
    for i in range(3):
        _, class_day = input_option(WEEK_DAYS, prompt="Select a class day")
        days[i] = class_day
        print()
    days.sort()
    return days


def preprocess_states(ds: DataStore, history: History) -> None:
    history.set_cohort(ds)
    history.set_class_days(input_class_days(), start=None)
    date_cols: list[str] = history.str_dates()
    ds.data[date_cols] = RecordStatus.EMPTY
