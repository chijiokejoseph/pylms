from typing import Callable

import pandas as pd

from pylms.constants import DATA_COLUMNS, NA_COLUMNS_FILL
from pylms.utils.data import DataStream

type Validator = Callable[[pd.DataFrame], bool]


def clean_na(
    data_stream: DataStream[pd.DataFrame], validate_na_removal: Validator | None = None
) -> DataStream[pd.DataFrame]:
    """
    Removes missing or N/A values in the underlying data of the input DataStream.

        type Validator = Callable[[pd.DataFrame], bool]

    :param data_stream: ( DataStream[pd.DataFrame] ) : Input DataStream containing the data to be cleaned
    :type: DataStream[pd.DataFrame]
    :param validate_na_removal: ( Validator | None, optional ): A function that implements a custom validation function to check that the processed data does not have any missing values. It Defaults to None
    :type validate_na_removal: Validator | None

    :rtype: DataStream[pd.DataFrame]
    :return: cleaned data as DataStream
    """

    data: pd.DataFrame = data_stream()
    data = data.fillna(NA_COLUMNS_FILL)

    def validate(test_data: pd.DataFrame) -> bool:
        test1: bool = test_data.isna().any().any()
        if test1:
            return False
        columns_list: list[str] = test_data.columns.tolist()
        test2: bool = all([each_col in DATA_COLUMNS for each_col in columns_list])
        return test2

    if validate_na_removal is None:
        validate_na_removal = validate

    return DataStream(data, validate_na_removal)
