from pylms.constants import COHORT, DATE, DATE_FMT
from pylms.utils.data import DataStream
from datetime import datetime
import re
import pandas as pd


def clean_cohort(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    from pylms.cli import input_num
    msg: str = "\nCleaning Cohort in preprocessing stage... \nPlease enter the cohort number for this current cohort: "

    def validator(num: float | int) -> bool:
        return num > 0

    cohort_no: float | int = input_num(msg, "int", validator)
    data = data_stream()
    data[COHORT] = cohort_no
    return DataStream(data)


def clean_date(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    from pylms.cli import input_str
    msg: str = "Cleaning Cohort in preprocessing stage... \nPlease enter the orientation date for this current cohort. \nIt should be of the form dd/mm/yyyy: "

    test_date: str = f"01/01/{datetime.now().year}"
    bad_pattern_msg: str = (
        "Your input does not match the specified pattern of dd/mm/yyyy."
    )
    invalid_date_msg: str = f"Entered date is behind {test_date}, the orientation date of the cohort. How is that possible?"
    diagnosis_map: dict[str, str] = {"result": ""}

    def validator(str_input: str) -> bool:
        pattern: re.Pattern = re.compile(r"\d{2}/\d{2}/\d{4}")
        matches: re.Match | None = pattern.match(str_input)
        if matches is None:
            diagnosis_map["result"] = bad_pattern_msg
            return False
        start_date: datetime = datetime.strptime(str_input, DATE_FMT)
        if start_date < datetime.strptime(test_date, DATE_FMT):
            diagnosis_map["result"] = invalid_date_msg
            return False
        return True

    cohort_date: str = input_str(msg, validator, diagnosis=diagnosis_map["result"])
    data = data_stream()
    data[DATE] = cohort_date
    return DataStream(data)
