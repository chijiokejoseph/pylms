from collections.abc import Callable

import polars as pl

from ..constants import COMMA_DELIM


def val_cols_data(test_data: pl.DataFrame, req_cols: list[str]) -> tuple[bool, str]:
    column_list = test_data.columns
    missing_cols = [column for column in column_list if column not in req_cols]

    if len(missing_cols) > 0:
        cols_print = COMMA_DELIM.join(missing_cols)
        msg = f"Data is missing the following columns: '{cols_print}'"
        return False, msg

    return True, ""


def new_validator(req_cols: list[str]) -> Callable[[pl.DataFrame], tuple[bool, str]]:
    def validator(test_data: pl.DataFrame) -> tuple[bool, str]:
        return val_cols_data(test_data, req_cols)

    return validator
