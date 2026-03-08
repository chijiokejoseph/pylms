import polars as pl

from pylms.info import print_info

from ..cli import input_num, input_option
from ..data import DataStore
from ..errors import Result
from ..query_data import run_query_data
from ..result_utils import det_result_col


def edit_multiple(ds: DataStore, result_data: pl.DataFrame) -> Result[list[float]]:
    result_col: str = det_result_col()
    student_serials = run_query_data(ds)
    if student_serials.is_err():
        return student_serials.propagate()

    student_serials = student_serials.unwrap()

    num_rows: int = result_data.height
    updates_list: list[float] = [0.0] * num_rows

    for each_serial in student_serials:
        index: int = each_serial - 1
        student_record = result_data.row(index, named=True)
        student_score: float = result_data[index, result_col]
        print_info("Target Record")
        for key, value in student_record.items():
            print_info(f"{key}: {value}")
        print()

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
                result_data[index, result_col] = score if score <= 100 else 100
                updates_list[index] = marks
            case _:
                result_data[index, result_col] = student_score - marks
                updates_list[index] = -marks

    return Result.ok(updates_list)
