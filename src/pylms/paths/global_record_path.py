from pathlib import Path

from ..constants import GLOBAL_RECORD_JSON
from .path_fns import get_data_path


def get_global_record_path() -> Path:
    return get_data_path() / GLOBAL_RECORD_JSON
