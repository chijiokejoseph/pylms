from pylms.utils.date._add_dates import _add_dates
from pylms.utils.date._save_dates import _save_dates
from pylms.utils.data import DataStore


def prepare_dates(ds: DataStore, num_weeks: int = 5) -> None:
    from pylms.history import History

    history: History = History.load()
    history.replan_weeks(num_weeks)
    class_dates: list[str] = history.str_dates()
    _add_dates(ds, class_dates)
    _save_dates(class_dates)
    print(
        "Dates for the classes have been prepared successfully \nA template attendance for each of the classes has been added accordingly."
    )
