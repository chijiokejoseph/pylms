import pandas as pd
import numpy as np
from pylms.clean_pipeline.errors import HasDuplicatesErr, MissingColsErr
import re

from pylms.constants import REGISTRATION_COLS


def verify(test_data: pd.DataFrame) -> None:
    cols: list[str] = test_data.columns.tolist()
    # reject data if it has duplicates
    if test_data.columns.has_duplicates:
        duplicates: np.ndarray = test_data.columns.duplicated()
        raise HasDuplicatesErr(
            f"Registration data has duplicate cols {duplicates.tolist()}"
        )

    for required_col in REGISTRATION_COLS:
        _verify_required_col(cols, required_col)


def _verify_col_name(col_name: str, expected: str) -> bool:
    return re.compile(expected, re.IGNORECASE).search(col_name) is not None


def _verify_required_col(col_names: list[str], required_col: str) -> None:
    if any(_verify_col_name(col_name, required_col) for col_name in col_names):
        return None
    else:
        raise MissingColsErr(f"Column {required_col} not found in registration data.")
