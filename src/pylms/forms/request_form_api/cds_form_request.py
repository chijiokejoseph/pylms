from pylms.forms.request_form_api.cds_form_init import init_cds_form
from pylms.utils import DataStore
from pylms.history import History


def request_cds_form(ds: DataStore, history: History) -> None:
    init_cds_form(ds, history)
    return None
