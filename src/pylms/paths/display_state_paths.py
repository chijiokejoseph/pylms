from pathlib import Path
from typing import Literal

from ..cli_utils import emphasis
from ..config import Config
from ..constants import CONFIG_JSON
from ..info import printpass
from .history_path import get_history_path
from .path_fns import get_data_path, get_paths_excel


def display_path(
    config: Config, state: Literal["History", "DataStore", "Config"]
) -> None:
    if state == "History":
        path = get_history_path(config)
    elif state == "Config":
        path = Path(config.data_dir) / CONFIG_JSON
    else:
        path = get_paths_excel(config)["DataStore"]

    data_path = get_data_path(config)
    path_display = str(path).replace(str(data_path), "...DATA")
    path_display = emphasis(path_display)
    printpass(f'{state} saved at path "{path_display}"')
