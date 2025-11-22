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
        return result.propagate()
    idx, choice = result.unwrap()
    print(f"You have selected {choice}")
    result = input_num(
        f"For {choice}, enter the number of marks: ",
        1.0,
        lambda x: x > 0,
        "The value entered is not greater than zero.",
    )
    if result.is_err():
        return result.propagate()

    marks = result.unwrap()
    match idx:
        case 1:
            result_data[result_col] += marks
            updates_list = [marks] * num_rows
        case _:
            result_data[result_col] -= marks
            updates_list = [-marks] * num_rows
    return Result.ok(updates_list)
