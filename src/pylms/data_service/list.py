from pathlib import Path

from ..constants import COHORT, DATA_COLUMNS
from ..data import DataStore, write
from ..errors import Result, Unit
from ..info import printpass
from ..paths import get_list_path


def list_ds(ds: DataStore) -> Result[Unit]:
    pretty = ds.pretty()
    cohort: int = pretty[0, COHORT]
    records = pretty[DATA_COLUMNS]

    save_path: Path = get_list_path(cohort)

    result = write(records, save_path)
    if result.is_err():
        return result.propagate()

    printpass(f"Students Data printed to path {save_path}\n")
    return Result.unit()
