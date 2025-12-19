from pathlib import Path

import numpy as np
import pandas as pd

from ..data import DataStream, read
from ..errors import Result, Unit, eprint
from ..history import History, record_result
from ..paths import get_paths_excel
from ..result_utils import (
    det_assessment_overall_col,
    det_assessment_req_col,
    det_assessment_score_col,
    det_passmark_col,
    det_project_overall_col,
    det_project_score_col,
    det_result_col,
)
from .input_collate_req import CollateReq, input_collate_req


def collate_result(history: History) -> Result[Unit]:
    """
    Collate the result spreadsheet for the students.

    The result spreadsheet should have the pass mark, assessment scores, project scores and overall scores.
    The assessment scores and project scores should be multiplied by the assessment ratio and project ratio respectively before being added together to get the overall scores.

    The user is prompted to enter the pass mark, assessment ratio and project ratio for the cohort.
    The entered data is validated before being saved to the Result.xlsx file in the Data folder.

    :param ds: (DataStore) - The data to be collated
    :type ds: DataStore
    :param history: (History) - The state of the application
    :type history: History

    :return: (Result[Unit]) - a result object
    :rtype: Result[Unit]
    """
    # Check if all required data (attendance, assessment, and project) has been collated
    if not history.has_collated_all:
        msg = "\nPlease collate attendance, assessment and project first\n"
        eprint(msg)
        return Result.err(msg)

    # Read the collated project data
    collated_data = read(get_paths_excel()["Project"])
    if collated_data.is_err():
        return collated_data.propagate()
    collated_data = collated_data.unwrap()

    # Prompt for and validate the pass mark, assessment ratio, and project ratio
    req_result = input_collate_req()
    if req_result.is_err():
        return req_result.propagate()

    req: CollateReq = req_result.unwrap()

    (pass_mark, assessment_ratio, project_ratio) = req

    # Retrieve column names for assessment and project scores
    assessment_score_col: str = det_assessment_score_col()

    assessment_req_col: str = det_assessment_req_col()
    project_score_col: str = det_project_score_col()
    passmark_col: str = det_passmark_col()

    # Scale assessment and project scores by their respective ratios
    collated_data.loc[
        :, [assessment_score_col, assessment_req_col, project_score_col]
    ] = collated_data.loc[
        :, [assessment_score_col, assessment_req_col, project_score_col]
    ].astype(float)

    collated_data.loc[:, assessment_score_col] *= assessment_ratio
    collated_data.loc[:, assessment_req_col] *= assessment_ratio
    collated_data.loc[:, project_score_col] *= project_ratio

    # Calculate overall scores by summing the scaled assessment and project scores
    assessment_data: pd.Series = collated_data[assessment_score_col]
    project_data: pd.Series = collated_data[project_score_col]
    score_data: pd.Series = project_data + assessment_data
    score_arr: np.ndarray = score_data.to_numpy()
    score_arr = np.array(
        [score if score <= 100 else 100 for score in score_arr.tolist()]
    ).round(2)

    # Rename columns to reflect overall scores
    new_assessment_col: str = det_assessment_overall_col(assessment_ratio)
    new_project_col: str = det_project_overall_col(project_ratio)
    collated_data = collated_data.rename(
        columns={
            assessment_score_col: new_assessment_col,
            project_score_col: new_project_col,
        }
    )

    # Add overall scores and pass mark to the collated data
    result_col: str = det_result_col()
    collated_data[result_col] = score_arr
    collated_data[passmark_col] = pass_mark

    # Save the collated result data to an Excel file
    result_stream: DataStream[pd.DataFrame] = DataStream(collated_data)
    result_path: Path = get_paths_excel()["Result"]
    result_stream.to_excel(result_path)

    # Record the result in the history
    record_result(history)

    return Result.unit()
