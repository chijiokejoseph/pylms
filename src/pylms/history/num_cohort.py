from datetime import datetime

from ..constants import COHORT, DATE, DATE_FMT
from ..data import DataStore
from ..errors import Result, Unit
from .days_cohort import update_dates
from .history import History


def set_cohort(history: History, ds: DataStore) -> Result[Unit]:
    history.orientation_date = datetime.strptime(
        ds.data[DATE].astype(str).iloc[0], DATE_FMT
    )
    history.cohort = ds.data[COHORT].astype(int).tolist()[0]
    return update_dates(history)
