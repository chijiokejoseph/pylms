from pathlib import Path
from pylms.utils.paths.path_fns import get_data_path
from pylms.constants import GLOBAL_RECORD_JSON


def get_global_record_path() -> Path:
    return get_data_path() / GLOBAL_RECORD_JSON