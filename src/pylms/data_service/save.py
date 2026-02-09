from pathlib import Path

from ..data import DataStore
from ..errors import Result, Unit, eprint
from ..paths import get_paths_excel


def save_ds(ds: DataStore) -> Result[Unit]:
    """Save DataStore to file.

    Args:
        ds (DataStore): DataStore to save.

    Returns:
        Result[Unit]: Success or error message.
    """
    from ..paths_state import display_path

    if ds.prefilled:
        msg = "Error: DataStore is prefilled and has no actual data"
        eprint(msg)
        return Result.err(msg)

    ds_path: Path = get_paths_excel()["DataStore"]

    result = ds.write(ds_path)
    if result.is_err():
        return result.propagate()

    # Display save path with abbreviated format
    display_path("DataStore")
    return Result.unit()
