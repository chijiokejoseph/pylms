from pylms.utils import DataStore
import pandas as pd
from pylms.data_ops.append_utils import clean_after_ops


def sub(superset: DataStore, serial: list[int]) -> None:
    drop_num: list[int] = [value - 1 for value in serial]
    data_ref: pd.DataFrame = superset.as_ref()
    data_ref.drop(index=drop_num, inplace=True)
    clean_after_ops(superset)
    return
