from typing import cast

import pandas as pd

from pylms.constants import RESULT_UPDATE, ValidateDataFn
from pylms.lms.utils import det_result_col, find_col, val_result_data
from pylms.utils import DataStream


def recollate(
    results_stream: DataStream[pd.DataFrame],
) -> DataStream[pd.DataFrame]:
    results = results_stream()
    results_stream = DataStream(results, cast(ValidateDataFn, val_result_data))

    score_cols = [
        find_col(results_stream, "Assessment", "Score").unwrap(),
        find_col(results_stream, "Project", "Score").unwrap(),
    ]

    results = results_stream()
    update_cols = [
        col for col in results.columns.tolist() if col.find(RESULT_UPDATE) != -1
    ]
    score_cols.extend(update_cols)
    scores = results.loc[:, score_cols]
    new_scores = scores.sum(axis=1)
    new_scores = pd.Series(
        [score if score <= 100 else 100 for score in new_scores.astype(float).tolist()]
    )
    results.loc[:, det_result_col()] = new_scores
    return DataStream(results)
