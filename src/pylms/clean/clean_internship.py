import pandas as pd

from ..constants import INTERNSHIP
from ..data import DataStream


def clean_internship(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    """Normalize internship values to uppercase and provide validation.

    This function converts all values in the column named by the module-level
    `INTERNSHIP` constant to upper-case strings. It returns a `DataStream`
    wrapping the transformed DataFrame and supplies a validator that ensures
    the `INTERNSHIP` column exists and that every value in the column is
    uppercase.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame to normalize.

    Returns:
        DataStream[pd.DataFrame]: A DataStream wrapping the normalized DataFrame.
    """
    data: pd.DataFrame = data_stream()

    data[INTERNSHIP] = data[INTERNSHIP].apply(str.upper)  # pyright: ignore [reportUnknownMemberType]

    def validate(test_data: pd.DataFrame) -> bool:
        """Return True when the internship column exists and entries are uppercase.

        Args:
            test_data (pd.DataFrame): DataFrame to validate.

        Returns:
            bool: True if `INTERNSHIP` is present in `test_data` and all values
                in that column are uppercase strings.
        """
        test1: bool = INTERNSHIP in test_data.columns.tolist()
        internship_col: list[str] = test_data[INTERNSHIP].tolist()
        test2: bool = all([row.isupper() for row in internship_col])
        return test1 and test2

    return DataStream(data, validate)
