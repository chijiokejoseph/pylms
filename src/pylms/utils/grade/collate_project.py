from pathlib import Path

import pandas as pd

from pylms.constants import GROUP, SCORE
from pylms.utils.data import DataStream
from pylms.utils.paths import get_paths_excel
from pylms.utils.grade.validators import (
    validate_attendance,
    validate_groups,
    validate_scores,
)


def collate_project(
    data_stream: DataStream[pd.DataFrame],
    percent: float,
) -> DataStream[pd.DataFrame]:
    groups_file: Path = get_paths_excel()["Group"]
    scores_file: Path = get_paths_excel()["Score"]
    groups: pd.DataFrame = pd.read_excel(groups_file)
    group_ds: DataStream = DataStream(groups, validate_groups)
    scores: pd.DataFrame = pd.read_excel(scores_file)
    score_ds: DataStream = DataStream(scores, validate_scores)

    scores_list: list[float] = []
    for index, row in group_ds().iterrows():
        group: int = row.loc[GROUP]
        score: float = score_ds()[SCORE].iloc[group - 1]
        score = score * percent
        score = round(score, 2)
        scores_list.append(score)

    old_data: pd.DataFrame = data_stream()
    column_name: str = f"Project {percent * 100:.2f}%"
    old_data[column_name] = scores_list
    return DataStream(old_data, validate_attendance)
