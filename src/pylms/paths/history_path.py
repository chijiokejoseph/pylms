from pathlib import Path

from ..config import Config
from ..constants import HISTORY_JSON
from .path_fns import get_data_path


def get_history_path(config: Config) -> Path:
    return get_data_path(config) / HISTORY_JSON
