from ..data import DataStore
from ..errors import Result, Unit
from ..history import History
from .update_form_init import init_update_form


def request_update_form(ds: DataStore, history: History) -> Result[Unit]:
    """Request creation of update form for student attendance.
    
    Args:
        ds (DataStore): DataStore containing student data.
        history (History): History object for tracking operations.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    return init_update_form(ds, history)
