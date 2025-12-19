from typing import cast

import pandas as pd

from ..cli import input_num, input_option
from ..cli.serials_input import provide_serials
from ..data import DataStore
from ..errors import Result
from ..result_utils import det_result_col


def edit_batch(ds: DataStore, result_data: pd.DataFrame) -> Result[list[float]]:
    # generate a very detailed documentation for the function in sphinx format
    """
    Edit the results of multiple students in a batch.
    This function allows the user to select multiple students and edit their results
    by either adding or subtracting marks. The user is prompted to select the type of edit
    (add or subtract) and to enter the number of marks to be added or subtracted.

    :param ds: (DataStore) - The DataStore object containing student data.
    :type ds: DataStore

    :param result_data: (pd.DataFrame) - The DataFrame containing the results of students.
    :type result_data: pd.DataFrame

    :return:
        A list of floats representing the updates made to the results of the students.
    :rtype: list[float]
    """

    print("Please provide serial numbers of students to reward/penalize their scores.")
    result: Result[list[int]] = provide_serials(ds)
    if result.is_err():
        print(f"Error providing serials: {result.unwrap_err()}")
        return Result[list[float]].err(result.unwrap_err())
    student_serials: list[int] = result.unwrap()

    # get the serial numbers and indices of the students to edit
    idxs: list[int] = [serial - 1 for serial in student_serials]

    # get the result column and number of rows
    num_rows: int = result_data.shape[0]
    result_col: str = det_result_col()

    # create a list to hold the updates
    updates_list: list[float] = [0.0] * num_rows

    # get the kind of edit to perform (add or subtract marks)
    options: list[str] = ["Add Marks", "Subtract Marks"]
    option_result = input_option(options)
    if option_result.is_err():
        return Result[list[float]].err(option_result.unwrap_err())
    idx, choice = option_result.unwrap()
    print(f"You have selected {choice}")

    # get the marks to add or subtract
    result_num = input_num(
        f"For {choice}, enter the number of marks: ",
        1.0,
        lambda x: x > 0,
        "The value entered is not greater than zero.",
    )
    if result.is_err():
        return Result[list[float]].err(result.unwrap_err())

    marks = result_num.unwrap()
    marks = marks if idx == 1 else -marks
    # apply the edit and record the updates
    for index in idxs:
        updates_list[index] = marks
        old_result: float = cast(float, result_data.loc[index, result_col])
        new_result: float = old_result + marks
        result_data.loc[index, result_col] = new_result if new_result <= 100 else 100
    return Result[list[float]].ok(updates_list)
