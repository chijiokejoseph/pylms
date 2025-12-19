from ..data import DataStore
from ..errors import Result, Unit
from ..history import History
from .update_form_init import init_update_form


def request_update_form(ds: DataStore, history: History) -> Result[Unit]:
    return init_update_form(ds, history)
