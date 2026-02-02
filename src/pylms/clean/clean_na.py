from typing import Callable

import polars as pl

from ..constants import COMMA_DELIM, DATA_COLUMNS, NA_COLUMNS_FILL
from ..data import DataStream
from ..errors import Result

type Validator = Callable[[pl.DataFrame], tuple[bool, str]]


def clean_na(
    data: pl.DataFrame, validate_na_removal: Validator | None = None
) -> Result[pl.DataFrame]:
    """Fill missing values and return a pl.DataFrame with a validator.

    Fill missing or N/A entries in the DataFrame contained in `data`
    using the module-level `NA_COLUMNS_FILL` mapping. The function returns a
    `pl.DataFrame` that carries a validator which ensures the processed DataFrame
    contains no missing values and only the expected columns defined in
    `DATA_COLUMNS`. A custom `validate_na_removal` function may be supplied to
    override the default validator.

    Args:
        data (pl.DataFrame): The
            DataFrame to be processed.
        validate_na_removal (Validator | None): Optional custom validator that
            accepts the processed DataFrame and returns True if validation
            succeeds. If None, a default validator is attached.

    Returns:
        Result[pl.DataFrame]: A Unit Result if the cleaning operation was successful
        or an `Result.err` value containing the validation error
    """

    data = data.with_columns(
        [
            pl.col(col).fill_null(fill).alias(col)
            if col in data.columns
            else pl.lit(fill).alias(col)
            for col, fill in NA_COLUMNS_FILL.items()
        ]
    )

    def validate(test_data: pl.DataFrame) -> tuple[bool, str]:
        test1 = test_data.filter(
            [pl.col(col).is_null().sum() > 0 for col in test_data.columns]
        )
        if test1.height > 0:
            return False, "Your data contains null values"
        columns: list[str] = test_data.columns

        missing_cols = [
            each_col for each_col in DATA_COLUMNS if each_col not in columns
        ]

        if len(missing_cols) == 0:
            return True, ""
        else:
            missing_print = COMMA_DELIM.join(missing_cols)
            return (
                False,
                f"The following columns: {missing_print} are required but are absent from your data",
            )

    if validate_na_removal is None:
        validate_na_removal = validate

    stream = DataStream.new(data, validate_na_removal)
    if stream.is_err():
        stream.print_if_err()

    stream = stream.unwrap().as_ref()

    return Result.ok(stream)
