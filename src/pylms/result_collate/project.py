import re
from pathlib import Path
from typing import Callable, cast

import numpy as np
import pandas as pd

from ..cli import input_path
from ..constants import GROUP, NAME, ValidateDataFn
from ..data import DataStream, read
from ..errors import Result, Unit, eprint
from ..history import History, record_project
from ..info import printpass
from ..paths import get_group_path, get_paths_excel
from ..result_utils import (
    det_project_score_col,
    val_assessment_data,
    val_attendance_data,
)


def _val_data(assessment_required: bool) -> Callable[[pd.DataFrame], bool]:
    if assessment_required:
        return val_assessment_data
    else:
        return val_attendance_data


def _val_input_data(test_data: pd.DataFrame) -> bool:
    columns_list: list[str] = test_data.columns.tolist()
    test_df_rows: int = test_data.shape[-2]
    num_groups: int = _extract_num_groups()
    if test_df_rows != num_groups:
        print(
            f"Project Groups created in the project are {num_groups} yet project scores received correspond to {test_df_rows} groups."
        )
        return False

    score_data: pd.Series = test_data.loc[:, columns_list[-1]]
    temp = score_data.dtype
    dtype_var: np.dtype = cast(np.dtype, temp)
    test = np.issubdtype(dtype_var, np.number)
    return test


def _extract_num_groups() -> int:
    group1_path: Path = get_group_path(1)
    parent: Path = group1_path.parent
    files: list[Path] = list(parent.iterdir())
    reg: re.Pattern[str] = re.compile(r"^Group\d+.xlsx$")
    group_files: list[Path] = [
        file for file in files if reg.match(file.name) is not None
    ]
    num_groups: int = len(group_files)
    return num_groups


def collate_project(history: History) -> Result[Unit]:
    """
    Collates the project scores for the students. Prompts the user to
    enter the path to the the project spreadsheet with:
    the expected number of groups with each row per project group

    The file should have one of the two formats:
        - 2-column: Group Number | Score
        - 3-column: Serial Number | Group Number | Score
    Note: Student names must match existing data in spelling and casing.

    :param history: (History) - The state of the application
    :type history: History

    :return: (Result[Unit]) - a result object
    :rtype: Result[Unit]


    """

    if not history.has_collated_assessment:
        msg = "\nAssessment has not been collated yet. Please collate the assessment first.\n"
        eprint(msg)
        return Result.err(msg)

    # Read the assessment data
    assessment_data = read(get_paths_excel()["Assessment"])
    if assessment_data.is_err():
        return assessment_data.propagate()
    assessment_data = assessment_data.unwrap()

    validate_data_fn: Callable[[pd.DataFrame], bool] = _val_data(True)
    data_stream = DataStream(assessment_data, validate_data_fn)
    data: pd.DataFrame = data_stream()

    # Get the project groups
    group_path: Path = get_group_path()
    if not group_path.exists():
        msg = "No groups have been created for this cohort. First Group the students for the cohort, and grade their scores before performing this operation."
        eprint(msg)
        return Result.err(msg)

    # Read the group data
    group_data = read(group_path)

    if group_data.is_err():
        return group_data.propagate()
    group_data = group_data.unwrap()

    # Get the number of groups
    num_groups: int = _extract_num_groups()

    # Prompt the user to enter the path to the project scores spreadsheet
    msg: str = f"""Please enter the (absolute) path to the project spreadsheet with:
{num_groups} rows, one per project group
The file should have one of the two formats:
    2-column: Group Number | Score
    3-column: Serial Number | Group Number | Score
Note: Student names must match existing data in spelling and casing.

Enter the path: """

    # Read the project scores spreadsheet
    result = input_path(msg)
    if result.is_err():
        return result.propagate()
    path = result.unwrap()

    print()

    project_df = read(path)

    if project_df.is_err():
        return project_df.propagate()
    project_df = project_df.unwrap()

    validate_fn = cast(ValidateDataFn, _val_input_data)
    project_stream: DataStream[pd.DataFrame] = DataStream(project_df, validate_fn)

    # Validate the input data
    project_df = project_stream()
    project_cols: list[str] = project_df.columns.tolist()

    # Determine the column name for the project scores
    match len(project_cols):
        case 2:
            score_col: str = project_cols[1]
        case 3:
            score_col = project_cols[2]
        case _:
            msg = "Wrong spreadsheet provided, expected spreadsheet to have 2 or 3 columns but requirement was not met."
            eprint(msg)
            return Result.err(msg)

    # Extract the project scores
    project_scores: pd.Series = project_df.loc[:, score_col]

    # Create a function to get the project score for a given student
    def get_group_score(
        names_list: list[str],
        groups_list: list[int],
        group_scores: list[float],
        name_in: str,
    ) -> float:
        name_idx: int = names_list.index(name_in)
        name_group: int = groups_list[name_idx]
        name_group_idx: int = name_group - 1
        name_score: float = group_scores[name_group_idx]
        return name_score

    # Get the names and groups from the data and group data
    names: pd.Series = data[NAME]
    groups: pd.Series = group_data[GROUP]

    # Get the project scores for each student
    assigned_scores: list[float] = [
        get_group_score(names.tolist(), groups.tolist(), project_scores.tolist(), name)
        for name in names.tolist()
    ]

    # Create a column in the data with the project scores
    project_col: str = det_project_score_col()
    data[project_col] = np.array(assigned_scores, dtype=np.float64).round(2)

    # Save the collated data to an Excel file
    printpass("Project Recorded Successfully\n")
    project_path: Path = get_paths_excel()["Project"]
    DataStream(data).to_excel(project_path)

    # Record the project in the history
    record_project(history)
    return Result.unit()
