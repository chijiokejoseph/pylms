from ..config import Config
from ..data import DataStore
from ..errors import Result, Unit
from ..history import History
from .cds_form_init import init_cds_form


def request_cds_form(config: Config, ds: DataStore, history: History) -> Result[Unit]:
    """Request creation of CDS form for NYSC corpers.
    
    Args:
        config (Config): Config containing facilitator information.
        ds (DataStore): DataStore containing student data.
        history (History): History object for tracking operations.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    return init_cds_form(config, ds, history)
