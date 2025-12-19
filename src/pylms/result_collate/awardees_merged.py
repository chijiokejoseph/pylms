from pathlib import Path

import numpy as np
import pandas as pd

from ..constants import AWARDEES, COHORT
from ..data import DataStore, DataStream, read
from ..errors import Result, Unit
from ..paths import get_fast_track_path, get_merged_path, get_merit_path


def _val_awardees(test_data: pd.DataFrame) -> bool:
    required_cols: list[str] = [
        AWARDEES["Batch"],
        AWARDEES["BatchID"],
        AWARDEES["CertID"],
        AWARDEES["CourseTitle"],
        AWARDEES["Date"],
        AWARDEES["Email"],
        AWARDEES["Name"],
        AWARDEES["Phone"],
    ]
    columns: list[str] = test_data.columns.tolist()
    return all(col in required_cols for col in columns)


def collate_merge(ds: DataStore) -> Result[Unit]:
    cohort_num: int = ds.as_ref()[COHORT].iloc[0]
    merged_path: Path = get_merged_path(cohort_num)

    fast_track_path: Path = get_fast_track_path(cohort_num)
    if not fast_track_path.exists():
        msg = "Cannot merge merit results with fast track results as fast track results do not exits."
        return Result.err(msg)

    fast_track_data = read(fast_track_path)
    if fast_track_data.is_err():
        return fast_track_data.propagate()
    fast_track_data = fast_track_data.unwrap()

    merit_path: Path = get_merit_path(cohort_num)
    if not merit_path.exists():
        msg = "Cannot merge fast track results with merit results as merit results do not yet exist."
        return Result.err(msg)

    merit_data = read(merit_path)
    if merit_data.is_err():
        return merit_data.propagate()
    merit_data = merit_data.unwrap()
    merit_data = DataStream(merit_data, _val_awardees)()

    fast_track_data = DataStream(fast_track_data, _val_awardees)()

    merged_data: pd.DataFrame = pd.concat((merit_data, fast_track_data))
    merged_data.dropna(inplace=True, how="all")  # pyright:ignore[reportUnknownMemberType]
    merged_data = merged_data.astype("str")
    merged_data = merged_data.replace("nan", "")  # pyright:ignore[reportUnknownMemberType]
    merged_data.drop_duplicates(
        subset=[AWARDEES["Email"], AWARDEES["Phone"]], inplace=True
    )

    name_col: str = AWARDEES["Name"]
    email_col: str = AWARDEES["Email"]

    merged_data[name_col] = merged_data[name_col].map(lambda x: x.strip().title())
    merged_data[email_col] = merged_data[email_col].map(lambda x: x.strip().lower())
    merged_data[AWARDEES["Phone"]] = merged_data[AWARDEES["Phone"]].astype(np.str_)
    merged_data.sort_values(by=AWARDEES["Name"], inplace=True)
    merged_data.reset_index(drop=True, inplace=True)
    DataStream(merged_data).to_excel(merged_path)
    return Result.unit()
