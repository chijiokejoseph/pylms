from pathlib import Path

from ..data import DataStore
from ..errors import Result
from ..info import print_info
from ..paths import get_paths_excel
from .prefill import prefill_ds


def load() -> Result[DataStore]:
    # get DataStore path
    path: Path = get_paths_excel()["DataStore"]

    # load DataStore from path if it exists
    # else return dummy DataStore
    if path.exists():
        init_ds = DataStore.from_local(path)
        if init_ds.is_err():
            return init_ds.propagate()

        init_ds = init_ds.unwrap()
    else:
        msg = "DataStore not found. Please register a new cohort first before performing any other operations."
        print_info(msg)
        return Result.ok(prefill_ds())

    return Result.ok(init_ds)
