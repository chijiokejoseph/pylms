import re

import pandas as pd

from ..constants import NAME, SERIAL, SPACE_DELIM, UNIQUE_COLUMNS
from ..data import DataStore
from ..record import RecordStatus


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


def clean_after_ops(ds: DataStore) -> None:
    data_ref: pd.DataFrame = ds.as_ref()
    data_ref.drop_duplicates(subset=UNIQUE_COLUMNS, keep="first", inplace=True)
    data_ref.sort_values(by=[NAME], inplace=True)
    data_ref.reset_index(drop=True, inplace=True)
    data_ref[SERIAL] = [i + 1 for i in range(data_ref.shape[0])]
    _clean_date(data_ref)
    return
