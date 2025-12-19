from ..data import DataStore
from ..errors import Result, Unit
from ..history import History
from .cds_form_init import init_cds_form


def request_cds_form(ds: DataStore, history: History) -> Result[Unit]:
    return init_cds_form(ds, history)
