from pathlib import Path

from ..config import Config
from ..constants import GLOBAL_RECORD_JSON
from .path_fns import get_data_path


def get_global_record_path(config: Config) -> Path:
    return get_data_path(config) / GLOBAL_RECORD_JSON
