from pathlib import Path
from typing import Literal, cast

import pandas as pd

from pylms.constants import (
    AWARDEES,
    AWARDEES_BATCH,
    AWARDEES_EMTPY,
    AWARDEES_ORDER,
    COHORT,
    EMAIL,
    NAME,
    PHONE,
    ValidateDataFn,
)
from pylms.config import read_course_name
from pylms.lms.utils import (
    fmt_date,
    fmt_phone,
)
from pylms.errors import LMSError
from pylms.utils import DataStream, date, paths

type CollateType = Literal["merit", "fast track"]


def collate_awardees(
    stream: DataStream[pd.DataFrame], collate_type: CollateType = "merit"
) -> None:
    def validate_fn(test_data: pd.DataFrame) -> bool:
        columns: list[str] = test_data.columns.tolist()
        req_cols: list[str] = [EMAIL, NAME, PHONE, COHORT]
        return all([req_col in columns for req_col in req_cols])

    stream = DataStream(stream(), cast(ValidateDataFn, validate_fn))
    data: pd.DataFrame = stream()
    dates_list: list[str] = date.retrieve_dates()
    end_date: str = dates_list[-1]
    end_date = fmt_date(end_date)
    cohort_num: int = data[COHORT].iloc[0]

    course_name: str = read_course_name()
    if course_name is None:
        raise LMSError("Course name has not been set in `state.toml`")

    len(AWARDEES_ORDER)
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
        paths.get_merit_path(cohort_num)
        if collate_type == "merit"
        else paths.get_fast_track_path(cohort_num)
    )
    awardees_stream: DataStream[pd.DataFrame] = DataStream(awardees_data)
    awardees_stream.to_excel(awardees_path)
