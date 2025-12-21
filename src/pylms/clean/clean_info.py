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
    """Prompt for and assign a cohort number to the DataStream.

    Prompts the user to enter the cohort number using `input_num` and validates
    that the provided value is a positive number. On success, the cohort value
    is written to the column specified by the `COHORT` constant and the
    updated DataFrame is returned wrapped in `Result.ok(DataStream(...))`.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame to update with the cohort number.

    Returns:
        Result[DataStream[pd.DataFrame]]: Ok result wrapping the DataStream
            containing the assigned cohort number, or an error `Result`
            propagated from the input prompt if validation fails.
    """
    msg: str = "\nCleaning Cohort in preprocessing stage... \nPlease enter the cohort number for this current cohort: "

    def validator(num: float | int) -> bool:
        """Validate that the cohort number is positive.

        Args:
            num (float | int): Candidate cohort number provided by the user.

        Returns:
            bool: True when `num` is greater than zero.
        """
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
    """Prompt for and validate the cohort orientation date, then assign it.

    Prompts the user to enter the orientation date for the cohort. The
    expected format is `dd/mm/yyyy`. The function validates both the textual
    format and that the entered date is not earlier than a minimal allowed
    date (constructed as `01/01/<current_year>`). If validation succeeds, the
    date is written to the column specified by `DATE` and the updated
    DataFrame is returned wrapped in `Result.ok(DataStream(...))`.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame to update with the cohort orientation date.

    Returns:
        Result[DataStream[pd.DataFrame]]: Ok result wrapping the DataStream
            with the assigned date, or an error `Result` propagated from the
            input prompt if validation fails.
    """
    from ..cli import input_str

    msg: str = "Cleaning Cohort in preprocessing stage... \nPlease enter the orientation date for this current cohort. \nIt should be of the form dd/mm/yyyy: "

    test_date: str = f"01/01/{datetime.now().year}"

    bad_pattern_msg: str = (
        "Your input does not match the specified pattern of dd/mm/yyyy."
    )

    invalid_date_msg: str = f"Entered date is behind {test_date}, the orientation date of the cohort. How is that possible?"

    diagnosis_map: dict[str, str] = {"result": ""}

    def validator(str_input: str) -> bool:
        """Validate an input date string is `dd/mm/yyyy` and not before `test_date`.

        This nested validator updates `diagnosis_map['result']` with a
        user-friendly message describing the validation failure if any.

        Args:
            str_input (str): Candidate date string provided by the user.

        Returns:
            bool: True when `str_input` matches the `dd/mm/yyyy` pattern and
                represents a date on or after `test_date`.
        """
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
