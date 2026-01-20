import numpy as np
import polars as pl

from pylms.data import DataStream, datamap

from ..constants import PHONE
from ..errors import Result
from ..re_phone import match_and_clean


def clean_phone(data: pl.DataFrame) -> Result[pl.DataFrame]:
    """Normalize phone numbers in the pl.DataFrame's DataFrame.

    This function validates that the input DataFrame contains a column named
    by the `PHONE` constant, that the column contains non-missing string
    values, and then applies the `match_and_clean` phone-normalization helper
    to each value.

    Args:
        data (pl.DataFrame): The
            DataFrame whose phone column should be normalized.

    Returns:
        None
    """

    def validate_data(test_data: pl.DataFrame) -> tuple[bool, str]:
        """Validate that the DataFrame contains a cleanable phone column.

        The validator checks three things:
        - The column named by `PHONE` exists.
        - The column contains no missing values.
        - All values in the column are strings.

        Args:
            test_data (pl.DataFrame): The DataFrame to validate.

        Returns:
            bool: True if the DataFrame passes all validation checks,
                False otherwise.
        """

        # Test if `test_data` has a `PHONE` column
        test1: bool = PHONE in test_data.columns
        if not test1:
            return False, f"Column '{PHONE}' is missing"

        # Test if `test_data` does not contain any missing values
        test2: bool = (
            test_data[PHONE].is_null().any() and test_data[PHONE].is_nan().any()
        )
        if not test2:
            return False, f"Column '{PHONE}' contains missing values"

        @np.vectorize
        def is_str(data: object) -> bool:
            return isinstance(data, str)

        # Test that `test_data` only contains values of type `str`
        test3 = datamap(data[PHONE], PHONE, is_str, np.bool_, pl.Boolean()).all()
        if not test3:
            return True, f"Column '{PHONE} contains non-string values"

        return True, ""

    result = DataStream.verify(data, validate_data)
    if result.is_err():
        return result.propagate()

    data = datamap(data, PHONE, np.vectorize(match_and_clean), np.str_, pl.String())
    return Result.ok(data)
