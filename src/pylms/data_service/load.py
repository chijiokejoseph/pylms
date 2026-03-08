from pathlib import Path

from ..config import Config
from ..data import DataStore, read
from ..errors import Result
from ..info import print_info
from ..paths import get_paths_excel
from .prefill import prefill_ds


def load_ds(config: Config) -> Result[DataStore]:
    """Load DataStore from file or return prefilled DataStore if not found.

    Args:
        config: Application configuration.

    Returns:
        Result[DataStore]: Success with loaded or prefilled DataStore.
    """
    path: Path = get_paths_excel(config)["DataStore"]

    ds = prefill_ds()
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
