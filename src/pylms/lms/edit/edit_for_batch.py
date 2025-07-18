import pandas as pd
from pylms.utils import DataStore
from pylms.cli import input_num, input_option, select_student
from pylms.lms.utils import det_result_col
from typing import cast

def _edit_batch(ds: DataStore, result_data: pd.DataFrame) -> list[float]:
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
    
        
    # get the serial numbers and indices of the students to edit
    student_serials: list[int] = select_student(ds)
    idxs: list[int] = [serial - 1 for serial in student_serials]
    
    # get the result column and number of rows
    num_rows: int = result_data.shape[0]
    result_col: str = det_result_col()
    
    # create a list to hold the updates
    updates_list: list[float] = [0.0] * num_rows
    
    # get the kind of edit to perform (add or subtract marks)
    options: list[str] = ["Add Marks", "Subtract Marks"]
    idx, choice = input_option(options)
    print(f"You have selected {choice}")
    
    # get the marks to add or subtract
    marks_temp = input_num(
        f"For {choice}, enter the number of marks: ",
        "float",
        lambda x: x > 0,
        "The value entered is not greater than zero.",
    )
    marks: float = cast(float, marks_temp)
    
    
    # apply the edit and record the updates
    for index in idxs:
        marks = marks if idx == 0 else -marks
        updates_list[index] = marks
        old_result: float = cast(float, result_data.loc[index, result_col])
        result_data.loc[index, result_col] = old_result + marks
    return [marks]