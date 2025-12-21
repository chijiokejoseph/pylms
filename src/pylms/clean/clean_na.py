from typing import Callable

import numpy as np
import pandas as pd

from ..constants import DATA_COLUMNS, NA_COLUMNS_FILL
from ..data import DataStream

type Validator = Callable[[pd.DataFrame], bool]


def clean_na(
    data_stream: DataStream[pd.DataFrame], validate_na_removal: Validator | None = None
) -> DataStream[pd.DataFrame]:
    """Fill missing values and return a DataStream with a validator.

    Fill missing or N/A entries in the DataFrame contained in `data_stream`
    using the module-level `NA_COLUMNS_FILL` mapping. The function returns a
    `DataStream` that carries a validator which ensures the processed DataFrame
    contains no missing values and only the expected columns defined in
    `DATA_COLUMNS`. A custom `validate_na_removal` function may be supplied to
    override the default validator.

    Args:
        data_stream (DataStream[pd.DataFrame]): DataStream containing the
            DataFrame to be processed.
        validate_na_removal (Validator | None): Optional custom validator that
            accepts the processed DataFrame and returns True if validation
            succeeds. If None, a default validator is attached.

    Returns:
        DataStream[pd.DataFrame]: A DataStream wrapping the filled DataFrame and
            the validator used to assert the cleaning operation was successful.
    """

    data: pd.DataFrame = data_stream()
    data = data.fillna(NA_COLUMNS_FILL)  # pyright: ignore [reportUnknownMemberType]

    def validate(test_data: pd.DataFrame) -> bool:
        test1: np.bool = test_data.isna().any().any()
        if test1:
            return False
        columns_list: list[str] = test_data.columns.tolist()
        test2: bool = all([each_col in DATA_COLUMNS for each_col in columns_list])
        return test2

    if validate_na_removal is None:
        validate_na_removal = validate

    return DataStream(data, validate_na_removal)
