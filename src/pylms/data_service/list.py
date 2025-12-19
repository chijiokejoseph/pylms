from pathlib import Path

import pandas as pd

from ..constants import COHORT, DATA_COLUMNS
from ..data import DataStore, DataStream
from ..paths import get_list_path


def list_ds(ds: DataStore) -> None:
    data: pd.DataFrame = ds.pretty()
    cohort: int = data[COHORT].iloc[0]
    records: pd.DataFrame = data[DATA_COLUMNS]
    record_stream = DataStream(records)
    save_path: Path = get_list_path(cohort)
    record_stream.to_excel(save_path)
    print(f"\nStudents Data printed to path {save_path}\n")
    return None
