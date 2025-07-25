from pathlib import Path
from typing import Callable, cast

import numpy as np
import pandas as pd

from pylms.constants import AWARDEES, COHORT
from pylms.utils import DataStore, DataStream, paths, read_data


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


type ValidatorFn = Callable[[pd.DataFrame | pd.Series], bool]
validator = cast(ValidatorFn, _val_awardees)


def collate_merge(ds: DataStore) -> None:
    cohort_num: int = ds.as_ref()[COHORT].iloc[0]
    merged_path: Path = paths.get_merged_path(cohort_num)
    merit_path: Path = paths.get_merit_path(cohort_num)
    fast_track_path: Path = paths.get_fast_track_path(cohort_num)
    if not fast_track_path.exists():
        print(
            "Cannot merge merit results with fast track results as fast track results do not exits."
        )
        return
    if not merit_path.exists():
        print(
            "Cannot merge fast track results with merit results as merit results do not yet exist."
        )
        return
    merit_data: pd.DataFrame = read_data(merit_path)
    fast_track_data: pd.DataFrame = read_data(fast_track_path)
    merit_data = DataStream(merit_data, validator)()
    fast_track_data = DataStream(fast_track_data, validator)()
    merged_data: pd.DataFrame = pd.concat((merit_data, fast_track_data))
    merged_data.dropna(inplace=True, how="all")
    merged_data = merged_data.astype("str")
    merged_data = merged_data.replace("nan", "")
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
