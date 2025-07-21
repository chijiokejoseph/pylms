from typing import cast

import pandas as pd

from pylms.cli import input_num, input_option, select_student
from pylms.lms.utils import det_result_col
from pylms.utils import DataStore


def _edit_mutliple(ds: DataStore, result_data: pd.DataFrame) -> list[float]:
    result_col: str = det_result_col()
    student_serials: list[int] = select_student(ds)
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
        idx, choice = input_option(
            options, title="Edit Result", prompt="Choose how to edit this result"
        )
        print(f"You have selected {choice}")
        marks_temp = input_num(
            f"For {choice}, enter the number of marks: ",
            "float",
            lambda x: x > 0,
            "The value entered is not greater than zero.",
        )
        marks: float = cast(float, marks_temp)
        match idx:
            case 1:
                result_data.loc[index, result_col] = student_score + marks
                updates_list[index] = marks
            case _:
                result_data.loc[index, result_col] = student_score - marks
                updates_list[index] = -marks

    return updates_list
