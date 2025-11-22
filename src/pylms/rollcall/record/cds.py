import re
from typing import cast

import pandas as pd

from pylms.constants import CDS, NAME, WORK_DAYS
from pylms.record import RecordStatus
from pylms.utils import DataStore, DataStream, date


def record_cds(ds: DataStore, cds_data_stream: DataStream[pd.DataFrame]) -> None:
    pretty_data: pd.DataFrame = ds.pretty()
    data_ref: pd.DataFrame = ds.as_ref()
    cds_data: pd.DataFrame = cds_data_stream()

    cds_names: list[str] = cds_data[NAME].tolist()
    cds_names = [name.title() for name in cds_names]
    cds_days: list[str] = cds_data[CDS].tolist()

    for row_idx, row in data_ref.iterrows():
        idx: int = cast(int, row_idx)
        new_row: pd.Series = row.copy()
        each_name: str = pretty_data.iloc[idx].loc[NAME]
        if each_name not in cds_names:
            continue
        cds_name_idx: int = cds_names.index(each_name)
        cds_day: str = cds_days[cds_name_idx]
        if cds_day not in WORK_DAYS:
            continue
        cds_day_num: int = date.to_day_num(cds_day)

        for index in row.index.tolist():
            if re.fullmatch(r"^\d{2}/\d{2}/\d{4}", index) is None:
                continue
            date_col: str = index
            date_day_num: int = date.to_day_num(date_col)
            if (
                cds_day_num == date_day_num
                and new_row.at[date_col] != RecordStatus.NO_CLASS
            ):
                new_row.at[date_col] = RecordStatus.CDS
        data_ref.iloc[idx, :] = new_row

    return None
