from pathlib import Path
from pylms.constants import HISTORY_JSON
from pylms.utils.paths.path_fns import get_data_path

def get_history_path() -> Path:
    return get_data_path() / HISTORY_JSON