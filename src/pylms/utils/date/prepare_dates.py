from pylms.utils.date._add_dates import _add_dates
from pylms.utils.date._det_dates import _det_dates
from pylms.utils.date._save_dates import _save_dates
from pylms.utils.data import DataStore


def prepare_dates(ds: DataStore, num_weeks: int = 5) -> None:
    class_dates: list[str] = _det_dates(ds, num_weeks)
    _add_dates(ds, class_dates)
    _save_dates(class_dates)
    print(
        "Dates for the classes have been prepared successfully \nA template attendance for each of the classes has been added accordingly."
    )
