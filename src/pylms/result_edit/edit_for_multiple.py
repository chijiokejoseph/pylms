from typing import cast

import pandas as pd

from ..cli import input_num, input_option, select_student
from ..data import DataStore
from ..errors import Result
from ..result_utils import det_result_col


def edit_multiple(ds: DataStore, result_data: pd.DataFrame) -> Result[list[float]]:
    result_col: str = det_result_col()
    student_serials = select_student(ds)
    if student_serials.is_err():
        return student_serials.propagate()

    student_serials = student_serials.unwrap()

    num_rows: int = result_data.shape[0]
    updates_list: list[float] = [0.0] * num_rows

    for each_serial in student_serials:
        index: int = each_serial - 1
        temp = result_data.loc[index, :]
        student_record: pd.Series = cast(pd.Series, temp)
        student_score: float = cast(float, student_record[result_col])
        print("\nTarget Record")
        print(f"\n{student_record}\n")
        options: list[str] = ["Add Marks", "Subtract Marks"]
        option_result = input_option(
            options, title="Edit Result", prompt="Choose how to edit this result"
        )
        if option_result.is_err():
            return option_result.propagate()
        idx, choice = option_result.unwrap()
        print(f"You have selected {choice}")
        result: Result[float] = input_num(
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
                score: float = student_score + marks
                result_data.loc[index, result_col] = score if score <= 100 else 100
                updates_list[index] = marks
            case _:
                result_data.loc[index, result_col] = student_score - marks
                updates_list[index] = -marks

    return Result[list[float]].ok(updates_list)
