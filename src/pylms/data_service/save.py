from pathlib import Path

from pylms.cli_utils import emphasis

from ..data import DataStore
from ..errors import Result, Unit, eprint
from ..info import printpass
from ..paths import get_data_path, get_paths_excel


def save(ds: DataStore) -> Result[Unit]:
    if ds.prefilled:
        msg = "Error: DataStore is prefilled and has no actual data"
        eprint(msg)
        return Result.err(msg)

    data_path = get_data_path()
    ds_path: Path = get_paths_excel()["DataStore"]

    result = ds.to_excel(ds_path)
    if result.is_err():
        return result.propagate()

    path_display = str(ds_path).replace(str(data_path), "...DATA")
    path_display = emphasis(path_display)
    printpass(f'DataStore saved at path "{path_display}"')
    return Result.unit()
