import polars as pl

from pylms.data import DataStream

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

        return True, ""

    result = DataStream.verify(data, validate_data)
    if result.is_err():
        return result.propagate()

    data = data.with_columns(
        pl.col(PHONE)
        .cast(pl.String)
        .map_elements(match_and_clean, return_dtype=pl.String)
    )
    return Result.ok(data)
