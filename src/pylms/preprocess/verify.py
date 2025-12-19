import re

import numpy as np
import pandas as pd

from ..constants import REGISTRATION_COLS
from ..errors import eprint


def verify(test_data: pd.DataFrame) -> bool:
    cols: list[str] = test_data.columns.tolist()
    # reject data if it has duplicates
    if test_data.columns.has_duplicates:
        duplicates: np.ndarray = test_data.columns.duplicated()
        msg = f"Registration data has duplicate cols {duplicates.tolist()}"
        eprint(msg)
        return False

    if all(
        _verify_required_col(cols, required_col) for required_col in REGISTRATION_COLS
    ):
        return True
    else:
        return False


def _verify_col_name(col_name: str, expected: str) -> bool:
    return re.compile(expected, re.IGNORECASE).search(col_name) is not None


def _verify_required_col(col_names: list[str], required_col: str) -> bool:
    if any(_verify_col_name(col_name, required_col) for col_name in col_names):
        return True
    else:
        msg = f"Column {required_col} not found in registration data."
        eprint(msg)
        return False
