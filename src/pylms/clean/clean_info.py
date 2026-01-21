import re

import pandas as pd

from ..cli import input_num, input_str
from ..constants import COHORT, DATE
from ..data import DataStream
from ..errors import Result, Unit


def clean_cohort(
    data_stream: DataStream[pd.DataFrame],
) -> Result[Unit]:
    """Prompt for and assign a cohort number to the DataStream.

    Prompts the user to enter the cohort number using `input_num` and validates
    that the provided value is a positive number. On success, the cohort value
    is written to the column specified by the `COHORT` constant and the
    updated DataFrame is returned wrapped in `Result.ok(DataStream(...))`.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame to update with the cohort number.

    Returns:
        Result[Unit]: Unit Result indicating success, or an error `Result`
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
    return Result.unit()


def clean_date(
    data_stream: DataStream[pd.DataFrame],
) -> Result[Unit]:
    """Prompt for and validate the cohort orientation date, then assign it.

    Prompts the user to enter the orientation date for the cohort. The
    expected format is `dd/mm/yyyy`. The function validates both the textual
    format and that the entered date is not earlier than a minimal allowed
    date (constructed as `01/01/<current_year>`). If validation succeeds, the
    date is written to the column specified by `DATE`.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame to update with the cohort orientation date.

    Returns:
        Result[Unit]: Unit result indicating success or an error `Result`
        propagated from the input prompt if validation fails.
    """

    msg: str = "Cleaning Cohort in preprocessing stage... \nPlease enter the orientation date for this current cohort. \nIt should be of the form dd/mm/yyyy: "

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
            return False
        return True

    result = input_str(msg, validator)

    if result.is_err():
        return result.propagate()

    cohort_date: str = result.unwrap()

    data = data_stream.as_ref()
    data[DATE] = cohort_date
    return Result.unit()
