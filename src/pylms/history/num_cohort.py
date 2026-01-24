from datetime import datetime

from ..constants import COHORT, DATE, DATE_FMT
from ..data import DataStore
from ..errors import Result, Unit
from .classes import sync_classes
from .history import History


def set_cohort(history: History, ds: DataStore) -> Result[Unit]:
    """Set cohort information and orientation date from DataStore.
    
    Args:
        history (History): History instance to update.
        ds (DataStore): DataStore containing cohort and date information.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    data_ref = ds.as_ref()
    history.orientation_date = datetime.strptime(
        data_ref[0, DATE], DATE_FMT
    )
    history.cohort = data_ref[0, COHORT]
    return sync_classes(history)
