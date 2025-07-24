from pylms.constants import DATA_COLUMNS
from pylms.utils import DataStore
import pandas as pd
from pylms.data_ops.append_utils import _clean_up


def sub(superset: DataStore, serial: list[int]) -> DataStore:
    drop_num: list[int] = [value - 1 for value in serial]
    new_data: pd.DataFrame = superset().drop(index=drop_num)
    new_ds: DataStore = DataStore(new_data[DATA_COLUMNS])
    new_ds.data = new_data
    return _clean_up(new_ds)
