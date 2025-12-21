import pandas as pd

from ..constants import PHONE
from ..data import DataStream
from ..re_phone import match_and_clean


def clean_phone(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    """Normalize phone numbers in the DataStream's DataFrame.

    This function validates that the input DataFrame contains a column named
    by the `PHONE` constant, that the column contains non-missing string
    values, and then applies the `match_and_clean` phone-normalization helper
    to each value. The processed DataFrame is returned wrapped in a
    `DataStream`.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame whose phone column should be normalized.

    Returns:
        DataStream[pd.DataFrame]: A DataStream wrapping the DataFrame with the
            normalized phone numbers.
    """

    def validate_data(test_data: pd.DataFrame) -> bool:
        """Validate that the DataFrame contains a cleanable phone column.

        The validator checks three things:
        - The column named by `PHONE` exists.
        - The column contains no missing values.
        - All values in the column are strings.

        Args:
            test_data (pd.DataFrame): The DataFrame to validate.

        Returns:
            bool: True if the DataFrame passes all validation checks,
                False otherwise.
        """

        # Test if `test_data` has a `PHONE` column
        test1: bool = PHONE in test_data.columns.tolist()
        if not test1:
            return False

        # Test if `test_data` does not contain any missing values
        test2: bool = test_data[PHONE].notna().all().item()
        if not test2:
            return False

        def is_str(data: object) -> bool:
            return isinstance(data, str)

        # Test that `test_data` only contains values of type `str`
        test3: bool = test_data[PHONE].apply(is_str).all().item()  # pyright: ignore [reportUnknownMemberType]
        return test3

    valid_data: pd.DataFrame = DataStream(data_stream, validate_data)()
    valid_data[PHONE] = valid_data[PHONE].apply(match_and_clean)  # pyright: ignore [reportUnknownMemberType]
    return DataStream(valid_data)
