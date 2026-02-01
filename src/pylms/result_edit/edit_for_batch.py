import polars as pl

from ..cli import input_num, input_option
from ..cli.serials_input import provide_serials
from ..data import DataStore
from ..errors import Result
from ..result_utils import det_result_col


def edit_batch(ds: DataStore, result_data: pl.DataFrame) -> Result[tuple[pl.DataFrame, list[float]]]:
    """Edit results for multiple selected students with same adjustment.

    Allows user to select multiple students and apply the same mark adjustment
    (add or subtract) to all selected students.

    Args:
        ds (DataStore): DataStore containing student data for serial selection.
        result_data (pl.DataFrame): DataFrame containing student results to edit.

    Returns:
        Result[tuple[pl.DataFrame, list[float]]]: Success with new updated DataFrame and a list of updates applied to each student or error.
    """
    print("Please provide serial numbers of students to reward/penalize their scores.")
    result = provide_serials(ds)
    if result.is_err():
        return result.propagate()

    student_serials = result.unwrap()

    # Get indices (0-based) from serials (1-based)
    idxs = [serial - 1 for serial in student_serials]

    # Get result column and number of rows
    num_rows = result_data.height
    result_col = det_result_col()

    # Initialize updates list
    updates_list = [0.0] * num_rows

    # Get edit type (add or subtract marks)
    options = ["Add Marks", "Subtract Marks"]
    result = input_option(options)
    if result.is_err():
        return result.propagate()

    idx, choice = result.unwrap()
    print(f"You have selected {choice}")

    # Get marks to add or subtract
    result = input_num(
        f"For {choice}, enter the number of marks: ",
        1.0,
        lambda x: x > 0,
        "The value entered is not greater than zero.",
    )
    if result.is_err():
        return result.propagate()

    marks = result.unwrap()
    marks = marks if idx == 1 else -marks

    # Apply edits to selected students
    for index in idxs:
        updates_list[index] = marks
        # Get old result and calculate new result
        old_result: float = result_data[index, result_col]
        new_result = old_result + marks
        # Cap result at 100
        capped_result = min(new_result, 100) if new_result <= 100 else 100.0

        # Update the specific row
        result_data = result_data.with_columns(
            pl.when(pl.int_range(pl.len()) == index)
            .then(pl.lit(capped_result))
            .otherwise(pl.col(result_col))
            .alias(result_col)
        )

    return Result.ok((result_data, updates_list))
