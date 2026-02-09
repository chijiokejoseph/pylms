

from ..cli_utils import emphasis
from ..info import printpass
from ..paths import get_data_path, get_history_path, get_paths_excel

from typing import Literal


def display_path(state: Literal["History", "DataStore"]):
    if state == "History":
        path = get_paths_excel()["DataStore"]
    else:
        path = get_history_path()

    data_path = get_data_path()
    path_display = str(path).replace(str(data_path), "...DATA")
    path_display = emphasis(path_display)
    printpass(f'{state} saved at path "{path_display}"')
    pass