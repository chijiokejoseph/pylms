import re
from datetime import datetime

import pandas as pd

from ..cli import input_num
from ..constants import COHORT, DATE, DATE_FMT
from ..data import DataStream
from ..errors import Result


def clean_cohort(
    data_stream: DataStream[pd.DataFrame],
) -> Result[DataStream[pd.DataFrame]]:
    msg: str = "\nCleaning Cohort in preprocessing stage... \nPlease enter the cohort number for this current cohort: "

    def validator(num: float | int) -> bool:
        return num > 0

    result = input_num(msg, 1, validator)
    if result.is_err():
        return result.propagate()

    cohort_no: int = result.unwrap()

    data = data_stream()
    data[COHORT] = cohort_no
    return Result.ok(DataStream(data))


def clean_date(
    data_stream: DataStream[pd.DataFrame],
) -> Result[DataStream[pd.DataFrame]]:
    from ..cli import input_str

    msg: str = "Cleaning Cohort in preprocessing stage... \nPlease enter the orientation date for this current cohort. \nIt should be of the form dd/mm/yyyy: "

    test_date: str = f"01/01/{datetime.now().year}"

    bad_pattern_msg: str = (
        "Your input does not match the specified pattern of dd/mm/yyyy."
    )

    invalid_date_msg: str = f"Entered date is behind {test_date}, the orientation date of the cohort. How is that possible?"

    diagnosis_map: dict[str, str] = {"result": ""}

    def validator(str_input: str) -> bool:
        pattern: re.Pattern[str] = re.compile(r"\d{2}/\d{2}/\d{4}")
        matches: re.Match[str] | None = pattern.match(str_input)
        if matches is None:
            diagnosis_map["result"] = bad_pattern_msg
            return False
        start_date: datetime = datetime.strptime(str_input, DATE_FMT)
        if start_date < datetime.strptime(test_date, DATE_FMT):
            diagnosis_map["result"] = invalid_date_msg
            return False
        return True

    result = input_str(msg, validator, diagnosis=diagnosis_map["result"])

    if result.is_err():
        return result.propagate()

    cohort_date: str = result.unwrap()

    data = data_stream()
    data[DATE] = cohort_date
    return Result.ok(DataStream(data))
