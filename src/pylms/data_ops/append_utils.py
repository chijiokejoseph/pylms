import re

import pandas as pd

from pylms.constants import NAME, SERIAL, SPACE_DELIM, UNIQUE_COLUMNS
from pylms.record import RecordStatus
from pylms.utils import DataStore


def _clean_date(data: pd.DataFrame):
    def fill_space(entry: str) -> str:
        if entry != SPACE_DELIM:
            return entry
        return RecordStatus.PRESENT

    for column in data.columns.tolist():
        if re.fullmatch(r"^\d{2}/\d{2}/\d{4}$", column) is None:
            continue
        unique_values: list[str] = data[column].unique().flatten().tolist()
        if RecordStatus.EXCUSED in unique_values:
            continue
        if RecordStatus.ABSENT in unique_values:
            continue
        if RecordStatus.NO_CLASS in unique_values:
            data[column] = RecordStatus.NO_CLASS
            continue
        if RecordStatus.PRESENT in unique_values:
            data.loc[:, column] = data[column].map(fill_space)


def _clean_up(ds: DataStore) -> DataStore:
    data: pd.DataFrame = ds()
    data = data.drop_duplicates(subset=UNIQUE_COLUMNS, keep="first")
    data = data.sort_values(by=[NAME])
    data = data.reset_index(drop=True)
    data[SERIAL] = [i + 1 for i in range(data.shape[0])]
    _clean_date(data)
    ds.data = data
    return ds
