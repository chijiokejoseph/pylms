import pandas as pd

from pylms.info import print_info

from ..cli import input_num, input_option, provide_serials
from ..data import DataStore
from ..errors import Result
from ..result_utils import det_result_col


def edit_multiple(ds: DataStore, result_data: pd.DataFrame) -> Result[list[float]]:
    result_col: str = det_result_col()
    student_serials = provide_serials(ds)
    if student_serials.is_err():
        return student_serials.propagate()

    student_serials = student_serials.unwrap()

    num_rows: int = result_data.shape[0]
    updates_list: list[float] = [0.0] * num_rows

    for each_serial in student_serials:
        index: int = each_serial - 1
        student_record = result_data.loc[index, :]
        student_score = result_data[result_col].astype(float).iloc[index]
        print_info("Target Record")
        print_info(f"{student_record}\n")

        options: list[str] = ["Add Marks", "Subtract Marks"]

        result = input_option(
            options, title="Edit Result", prompt="Choose how to edit this result"
        )
        if result.is_err():
            return result.propagate()
        idx, choice = result.unwrap()

        print_info(f"You have selected {choice}")
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
                score: float = student_score + marks
                result_data.loc[index, result_col] = score if score <= 100 else 100
                updates_list[index] = marks
            case _:
                result_data.loc[index, result_col] = student_score - marks
                updates_list[index] = -marks

    return Result.ok(updates_list)
