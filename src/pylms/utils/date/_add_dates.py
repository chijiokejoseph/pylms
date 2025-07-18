import pandas as pd

from pylms.record import RecordStatus
from pylms.utils.data import DataStore


def _add_dates(ds: DataStore, class_dates: list[str]) -> None:
    num_rows: int = ds().shape[0]
    data_dict: dict[str, list[RecordStatus]] = {
        date: [RecordStatus.EMPTY for _ in range(num_rows)] for date in class_dates
    }
    class_data: pd.DataFrame = pd.DataFrame(data=data_dict)
    ds_data: pd.DataFrame = ds()
    new_data: pd.DataFrame = pd.concat((ds_data, class_data), axis=1)
    ds.data = new_data
    return None
