from pathlib import Path
from typing import Callable, cast

import numpy as np
import pandas as pd

from pylms.cli import input_path, test_path_in
from pylms.constants import GROUP, NAME
from pylms.lms.collate.errors import NoProjectGroupsErr, SpreadSheetFmtErr
from pylms.lms.utils import (
    det_project_score_col,
    val_assessment_data,
    val_attendance_data,
)
from pylms.utils import DataStream, paths, read_data


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
    return cast(bool, test)


def _extract_num_groups() -> int:
    group1_path: Path = paths.get_group_path(1)
    parent: Path = group1_path.parent
    list_subfolders: list[Path] = list(parent.iterdir())
    num_groups: int = len(list_subfolders)
    return num_groups


def collate_project(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    type ValidateFn = Callable[[pd.DataFrame | pd.Series], bool]
    validate_data_fn: Callable[[pd.DataFrame], bool] = _val_data(True)
    validate_fn = cast(ValidateFn, validate_data_fn)
    data_stream = DataStream(data_stream(), validate_fn)
    data: pd.DataFrame = data_stream()

    group_path: Path = paths.get_group_path()
    if not group_path.exists():
        err_msg: str = "No groups have been created for this cohort. First Group the students for the cohort, and grade their scores before performing this operation."
        raise NoProjectGroupsErr(err_msg)

    group_data: pd.DataFrame = read_data(group_path)

    num_groups: int = _extract_num_groups()

    msg: str = f"""Enter the absolute path to the project scores excel spreadsheet for the students.
The entered spreadsheet should have {num_groups} rows corresponding to each project group.
The entered spreadsheet should take either of these two (2) formats:
    i. Two column spreadsheet
    ii. Three column spreadsheet

Two Column Spreadsheet:
    Here the data should have just two columns, the first column should contain the group numbers
    and the second column should contain their overall project scores graded to 100%.

Three Column Spreadsheet:
    Here the data unlike in the two columns has an extra column preceding both the group and scores columns
    which holds serial numbers or some 'S/N' data.

Please take note that the names of students in both cases must be spelt in the same arrangement and casing 
as the existing data.
Furthermore the entered path should be absolute and not relative.

Enter the path: """

    path: Path = input_path(
        msg,
        path_test_fn=test_path_in,
        path_test_diagnosis="The path entered does not exist, "
        "is not absolute or is not a valid excel file.",
    )
    print()
    project_df: pd.DataFrame = read_data(path)
    validate_fn = cast(ValidateFn, _val_input_data)
    project_stream: DataStream[pd.DataFrame] = DataStream(project_df, validate_fn)

    project_df = project_stream()
    project_cols: list[str] = project_df.columns.tolist()

    match len(project_cols):
        case 2:
            score_col: str = project_cols[1]
        case 3:
            score_col = project_cols[2]
        case _:
            raise SpreadSheetFmtErr(
                "Wrong spreadsheet provided, expected spreadsheet to have 2 or 3 columns but requirement was not met."
            )

    project_scores: pd.Series = project_df.loc[:, score_col]

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

    names: pd.Series = data[NAME]
    groups: pd.Series = group_data[GROUP]
    assigned_scores: list[float] = [
        get_group_score(names.tolist(), groups.tolist(), project_scores.tolist(), name)
        for name in names.tolist()
    ]

    project_col: str = det_project_score_col()
    data[project_col] = np.array(assigned_scores, dtype=np.float64).round(2)
    print("\nProject Recorded Successfully\n")
    return DataStream(data)
