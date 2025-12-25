from pathlib import Path

import pandas as pd

from ..constants import COHORT, DATA_COLUMNS
from ..data import DataStore, DataStream
from ..errors import Result, Unit
from ..info import printpass
from ..paths import get_list_path


def list_ds(ds: DataStore) -> Result[Unit]:
    data: pd.DataFrame = ds.pretty()
    cohort: int = data[COHORT].iloc[0]
    records: pd.DataFrame = data[DATA_COLUMNS]
    record_stream = DataStream(records)

    save_path: Path = get_list_path(cohort)

    result = record_stream.to_excel(save_path)
    if result.is_err():
        return result.propagate()

    printpass(f"Students Data printed to path {save_path}\n")
    return Result.unit()
