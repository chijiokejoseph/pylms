from typing import Literal

import polars as pl

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
from ..data import DataStream, new_validator
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
"""Type alias for awardees collation types.

Specifies whether to collate merit-based or fast-track awardees.
"""


def collate_awardees(
    stream: DataStream, cohort_num: int, collate_type: CollateType = "merit"
) -> Result[Unit]:
    """Collate awardees data for certificate generation.

    Processes student data to create awardees list with formatted information
    for certificate generation, supporting both merit and fast-track categories.

    Args:
        stream (DataStream): Stream containing student data.
        cohort_num (int): The cohort number to collate awardees for.
        collate_type (CollateType): Type of awardees to collate ("merit" or "fast track").

    Returns:
        Result[Unit]: Success or error with message.
    """

    validate_fn = new_validator([EMAIL, NAME, PHONE, COHORT])

    result = DataStream.verify(stream.as_ref(), validate_fn)
    if result.is_err():
        return result.propagate()

    data = stream.as_ref()
    dates_list = retrieve_dates("")
    if dates_list.is_err():
        return dates_list.propagate()

    dates_list = dates_list.unwrap()

    end_date = dates_list[-1]
    end_date = fmt_date(end_date)

    course_name = read_course_name()
    if course_name.is_err():
        return course_name.propagate()
    course_name = course_name.unwrap()

    awardees_data = pl.DataFrame(
        {
            AWARDEES["Email"]: data[EMAIL],
            AWARDEES["CourseTitle"]: pl.lit(course_name),
            AWARDEES["Date"]: pl.lit(end_date),
            AWARDEES["Name"]: data[NAME],
            AWARDEES["Phone"]: data[PHONE].map_elements(
                fmt_phone, return_dtype=pl.Utf8
            ),
            AWARDEES["Batch"]: pl.lit(AWARDEES_BATCH),
            AWARDEES["BatchID"]: pl.lit(AWARDEES_EMTPY),
            AWARDEES["CertID"]: pl.lit(AWARDEES_EMTPY),
        }
    )

    merit_path = get_merit_path(cohort_num)
    if merit_path.is_err():
        return merit_path.propagate()
    merit_path = merit_path.unwrap()

    fast_track_path = get_fast_track_path(cohort_num)
    if fast_track_path.is_err():
        return fast_track_path.propagate()
    fast_track_path = fast_track_path.unwrap()

    awardees_path = merit_path if collate_type == "merit" else fast_track_path

    awardees_stream = DataStream(awardees_data)

    result = awardees_stream.write(awardees_path)
    if result.is_err():
        return result.propagate()

    return Result.unit()
