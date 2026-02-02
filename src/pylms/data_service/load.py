from pathlib import Path

from ..data import DataStore, read
from ..errors import Result
from ..info import print_info
from ..paths import get_paths_excel
from .prefill import prefill_ds


def load_ds() -> Result[DataStore]:
    """Load DataStore from file or return prefilled DataStore if not found.

    Returns:
        Result[DataStore]: Success with loaded or prefilled DataStore.
    """
    # Get DataStore path
    path: Path = get_paths_excel()["DataStore"]

    ds = prefill_ds()
    # Load DataStore from path if it exists, else return dummy DataStore
    if not path.exists():
        msg = "DataStore not found. Please register a new cohort first before performing any other operations."
        print_info(msg)
        return Result.ok(ds)

    data = read(path)
    if data.is_err():
        return data.propagate()

    data = data.unwrap()
    result = ds.copy_from(data)
    if result.is_err():
        return result.propagate()

    return Result.ok(ds)
