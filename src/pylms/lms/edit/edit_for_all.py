from typing import cast

import numpy as np
import pandas as pd

from pylms.cli import input_num, input_option
from pylms.errors import Result
from pylms.lms.utils import det_result_col


def edit_all(result_data: pd.DataFrame) -> Result[list[float]]:
    num_rows: int = result_data.shape[0]
    result_col: str = det_result_col()
    options: list[str] = ["Add Marks", "Subtract Marks"]
    result = input_option(options)
    if result.is_err():
        return Result[list[float]].err(result.unwrap_err())
    idx, choice = result.unwrap()
    print(f"You have selected {choice}")
    result = input_num(
        f"For {choice}, enter the number of marks: ",
        "float",
        lambda x: x > 0,
        "The value entered is not greater than zero.",
    )
    if result.is_err():
        return Result[list[float]].err(result.unwrap_err())

    marks_temp = result.unwrap()
    marks: float = cast(float, marks_temp)
    result_data[result_col] = result_data[result_col].astype(np.float64)
    match idx:
        case 1:
            result_data[result_col] += marks
            updates_list = [marks] * num_rows
        case _:
            result_data[result_col] -= marks
            updates_list = [-marks] * num_rows
    return Result[list[float]].ok(updates_list)
