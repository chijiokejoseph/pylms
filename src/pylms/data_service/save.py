from pathlib import Path

from ..config import Config
from ..data import DataStore
from ..errors import Result, Unit, eprint
from ..paths import display_path, get_paths_excel


def save_ds(config: Config, ds: DataStore) -> Result[Unit]:
    """Save DataStore to file.

    Args:
        config: Application configuration.
        ds: DataStore to save.

    Returns:
        Result[Unit]: Success or error message.
    """
    if ds.prefilled:
        msg = "Error: DataStore is prefilled and has no actual data"
        eprint(msg)
        return Result.err(msg)

    ds_path: Path = get_paths_excel(config)["DataStore"]

    result = ds.write(ds_path)
    if result.is_err():
        return result.propagate()

    display_path(config, "DataStore")
    return Result.unit()
