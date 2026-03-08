from pathlib import Path
from typing import Callable

import polars as pl

from ..cli import input_path
from ..config import Config
from ..constants import GROUP
from ..data import DataStream, read, write
from ..errors import Result, Unit, eprint
from ..history import History, get_num_groups, record_project
from ..info import printpass
from ..paths import get_group_path, get_paths_excel
from ..result_utils import (
    det_project_score_col,
    val_assessment_data,
    val_attendance_data,
    val_project_in,
)


def val_assessment(
    assessment_required: bool,
) -> Callable[[pl.DataFrame], tuple[bool, str]]:
    if assessment_required:
        return val_assessment_data
    else:
        return val_attendance_data


def collate_project(config: Config, history: History) -> Result[Unit]:
    """
    Collates the project scores for the students. Prompts the user to
    enter the path to the the project spreadsheet with:
    the expected number of groups with each row per project group

    The file should have one of the two formats:
        - 2-column: Group Number | Score
        - 3-column: Serial Number | Group Number | Score
    Note: Student names must match existing data in spelling and casing.

    Args:
        config (Config): The configuration object
        history (History): The history object

    Returns:
        Result[Unit]: The result of the operation
    """
    paths = get_paths_excel(config)
    if not history.has_collated_assessment:
        msg = "Assessment has not been collated yet. Please collate the assessment first.\n"
        eprint(msg)
        return Result.err(msg)

    # Read the assessment data
    assessment_data = read(paths["Assessment"])
    if assessment_data.is_err():
        return assessment_data.propagate()
    assessment_data = assessment_data.unwrap()

    validator = val_assessment(True)
    data_stream = DataStream.new(assessment_data, validator)
    if data_stream.is_err():
        data_stream.print_if_err()
        return data_stream.propagate()

    data_stream = data_stream.unwrap()
    data = data_stream.as_ref()

    # Get the project groups
    group_path: Path = get_group_path(config)
    if not group_path.exists():
        msg = "No groups have been created for this cohort. First Group the students for the cohort, and grade their scores before performing this operation."
        eprint(msg)
        return Result.err(msg)

    # Read the group data
    group_data = read(group_path)
    if group_data.is_err():
        return group_data.propagate()

    group_data = group_data.unwrap()

    data = data.with_columns(pl.Series(group_data[GROUP]))

    # Get the number of groups
    num_groups = get_num_groups(history)

    # Prompt the user to enter the path to the project scores spreadsheet
    msg = f"""Please enter the (absolute) path to the project spreadsheet with:
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

    project = read(path)

    if project.is_err():
        return project.propagate()
    project = project.unwrap()

    def _val_project(proj: pl.DataFrame) -> tuple[bool, str]:
        return val_project_in(proj, history)

    project_stream = DataStream.new(project, _val_project)
    if project_stream.is_err():
        project_stream.print_if_err()
        return project_stream.propagate()

    project_stream = project_stream.unwrap()

    # Validate the input data
    project = project_stream.as_ref()
    project_cols = project.columns

    # Determine the column name for the project scores
    match len(project_cols):
        case 2 | 3:
            score_col = project_cols[-1]
        case _:
            msg = "Wrong spreadsheet provided, expected spreadsheet to have 2 or 3 columns but requirement was not met."
            eprint(msg)
            return Result.err(msg)

    # Extract the project scores
    # Create a column in the data with the project scores
    project_col = det_project_score_col()
    data = data.with_columns(pl.lit(0).alias(project_col))

    for i in range(1, project.height + 1):
        data = data.with_columns(
            [
                pl.when(pl.col(GROUP) == i)
                .then(pl.lit(project[i - 1, score_col]))
                .otherwise(pl.col(project_col))
                .alias(project_col)
            ]
        )

    data = data.drop(GROUP)

    # Save the collated data to an Excel file
    printpass("Project Recorded Successfully\n")
    project_path = paths["Project"]

    result = write(project, project_path)
    if result.is_err():
        return result.propagate()

    # Record the project in the history
    record_project(config, history)
    return Result.unit()
