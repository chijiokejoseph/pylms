import re
from typing import cast

import pandas as pd

from ..constants import CDS, NAME, WORK_DAYS
from ..data import DataStore, DataStream
from ..date import to_day_num
from ..record import RecordStatus


def record_cds(ds: DataStore, cds_data_stream: DataStream[pd.DataFrame]) -> None:
    pretty = ds.to_pretty()
    names = pretty.loc[:, NAME].astype(str)
    data_ref = ds.as_ref()
    cds_data = cds_data_stream()

    cds_names = cds_data[NAME].tolist()
    cds_names = [name.title() for name in cds_names]
    cds_days = cds_data[CDS].tolist()

    for idx, row in data_ref.iterrows():
        idx = cast(int, idx)
        new_row = row.copy()
        each_name = names.iloc[idx]

        if each_name not in cds_names:
            continue

        cds_name_idx: int = cds_names.index(each_name)
        cds_day: str = cds_days[cds_name_idx]

        if cds_day not in WORK_DAYS:
            continue

        cds_day_num: int = to_day_num(cds_day)

        for index in row.index:
            if re.fullmatch(r"^\d{2}/\d{2}/\d{4}", index) is None:
                continue
            date_col: str = index
            date_day_num: int = to_day_num(date_col)
            if cds_day_num == date_day_num and new_row.at[date_col] != str(
                RecordStatus.NO_CLASS
            ):
                new_row.at[date_col] = str(RecordStatus.CDS)

        data_ref.loc[idx, :] = new_row

    return None
