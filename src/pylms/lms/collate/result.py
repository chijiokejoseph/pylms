from pathlib import Path

import numpy as np
import pandas as pd

from pylms.lms.collate.assessment import collate_assessment
from pylms.lms.collate.attendance import (
    collate_attendance,
)
from pylms.lms.collate.input_collate_req import CollateReq, input_collate_req
from pylms.lms.collate.project import collate_project
from pylms.lms.utils import (
    det_assessment_overall_col,
    det_assessment_score_col,
    det_passmark_col,
    det_project_overall_col,
    det_project_score_col,
    det_result_col,
)
from pylms.utils import DataStore, DataStream, paths


def collate_result(ds: DataStore) -> None:
    collate_req: CollateReq = input_collate_req()
    pass_mark: float = collate_req.pass_mark
    attendance_req: float = collate_req.attendance_req
    assessment_req: float = collate_req.assessment_req
    assessment_ratio: float = collate_req.assessment_ratio
    project_ratio: float = collate_req.project_ratio

    collate_stream: DataStream[pd.DataFrame] = collate_attendance(ds, attendance_req)
    collate_stream = collate_assessment(collate_stream, assessment_req)
    collate_stream = collate_project(collate_stream)
    collated_data: pd.DataFrame = collate_stream()

    assessment_score_col: str = det_assessment_score_col()
    project_score_col: str = det_project_score_col()
    passmark_col: str = det_passmark_col()
    collated_data.loc[:, assessment_score_col] *= assessment_ratio
    collated_data.loc[:, project_score_col] *= project_ratio

    assessment_data: pd.Series = collated_data[assessment_score_col]
    project_data: pd.Series = collated_data[project_score_col]
    score_data: pd.Series = project_data + assessment_data
    score_arr: np.ndarray = score_data.to_numpy()
    score_arr = score_arr.round(2)

    new_assessment_col: str = det_assessment_overall_col(assessment_ratio)
    new_project_col: str = det_project_overall_col(project_ratio)
    collated_data = collated_data.rename(
        columns={
            assessment_score_col: new_assessment_col,
            project_score_col: new_project_col,
        }
    )

    result_col: str = det_result_col()
    collated_data[result_col] = score_arr
    collated_data[passmark_col] = pass_mark
    result_stream: DataStream[pd.DataFrame] = DataStream(collated_data)
    result_path: Path = paths.get_paths_excel()["Result"]
    result_stream.to_excel(result_path)
