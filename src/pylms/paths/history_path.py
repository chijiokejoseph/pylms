from pathlib import Path

from ..constants import HISTORY_JSON
from .path_fns import get_data_path


def get_history_path() -> Path:
    return get_data_path() / HISTORY_JSON
