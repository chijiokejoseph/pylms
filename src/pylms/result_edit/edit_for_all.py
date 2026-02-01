import polars as pl

from ..cli import input_num, input_option
from ..errors import Result
from ..result_utils import det_result_col


def edit_all(result_data: pl.DataFrame) -> Result[tuple[pl.DataFrame, list[float]]]:
    """Edit all students' results by adding or subtracting marks.

    Prompts user to choose between adding or subtracting marks,
    then applies the same change to all students.

    Args:
        result_data (pl.DataFrame): DataFrame containing student results.

    Returns:
        Result[tuple[pl.DataFrame, list[float]]]: Success with updated result DataFrame and a list of updates applied or error.
    """
    num_rows = result_data.height
    result_col = det_result_col()
    options = ["Add Marks", "Subtract Marks"]
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
            # Add marks
            updates_list = [marks] * num_rows
        case _:
            # Subtract marks
            marks = -marks
            updates_list = [marks] * num_rows
    
    # Update the result column
    result_data = result_data.with_columns(
        (pl.col(result_col) + marks).alias(result_col)
    )
    
    return Result.ok((result_data, updates_list))
