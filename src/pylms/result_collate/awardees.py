from pathlib import Path
from typing import Literal

import pandas as pd

from ..config import read_course_name
from ..constants import (
    AWARDEES,
    AWARDEES_BATCH,
    AWARDEES_EMTPY,
    COHORT,
    EMAIL,
    NAME,
    PHONE,
)
from ..data import DataStream
from ..errors import Result, Unit
from ..history import retrieve_dates
from ..paths import (
    get_fast_track_path,
    get_merit_path,
)
from ..result_utils import (
    fmt_date,
    fmt_phone,
)

type CollateType = Literal["merit", "fast track"]


def collate_awardees(
    stream: DataStream[pd.DataFrame], collate_type: CollateType = "merit"
) -> Result[Unit]:
    def validate_fn(test_data: pd.DataFrame) -> bool:
        columns: list[str] = test_data.columns.tolist()
        req_cols: list[str] = [EMAIL, NAME, PHONE, COHORT]
        return all([req_col in columns for req_col in req_cols])

    stream = DataStream(stream(), validate_fn)
    data: pd.DataFrame = stream()
    dates_list = retrieve_dates("")
    if dates_list.is_err():
        return dates_list.propagate()

    dates_list = dates_list.unwrap()

    end_date: str = dates_list[-1]
    end_date = fmt_date(end_date)
    cohort_num: int = data[COHORT].iloc[0]

    course_name = read_course_name()
    if course_name.is_err():
        return course_name.propagate()

    awardees_data: pd.DataFrame = pd.DataFrame(
        data={
            AWARDEES["Email"]: data[EMAIL],
            AWARDEES["CourseTitle"]: course_name,
            AWARDEES["Date"]: end_date,
            AWARDEES["Name"]: data[NAME],
            AWARDEES["Phone"]: data[PHONE].map(fmt_phone),
            AWARDEES["Batch"]: AWARDEES_BATCH,
            AWARDEES["BatchID"]: AWARDEES_EMTPY,
            AWARDEES["CertID"]: AWARDEES_EMTPY,
        }
    )
    awardees_path: Path = (
        get_merit_path(cohort_num)
        if collate_type == "merit"
        else get_fast_track_path(cohort_num)
    )
    awardees_stream: DataStream[pd.DataFrame] = DataStream(awardees_data)
    awardees_stream.to_excel(awardees_path)
    return Result.unit()
