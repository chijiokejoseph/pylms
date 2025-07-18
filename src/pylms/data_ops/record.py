from pathlib import Path

import pandas as pd

from pylms.constants import COHORT, DATA_COLUMNS
from pylms.utils import DataStore, DataStream, paths


def record(ds: DataStore) -> None:
    data: pd.DataFrame = ds.pretty()
    cohort: int = data[COHORT].iloc[0]
    records: pd.DataFrame = data[DATA_COLUMNS]
    record_stream: DataStream = DataStream(records)
    save_path: Path = paths.get_list_path(cohort)
    record_stream.to_excel(save_path)
    print(f"\nStudents Data printed to path {save_path}\n")
    return None
