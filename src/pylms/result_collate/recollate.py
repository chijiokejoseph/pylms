import polars as pl

from ..constants import RESULT_UPDATE
from ..data import DataStream
from ..errors import Result
from ..result_utils import det_result_col, find_col, val_result_data


def recollate(
    results_stream: DataStream,
) -> Result[DataStream]:
    result = DataStream.verify(results_stream.as_ref(), val_result_data)
    if result.is_err():
        return result.propagate()

    score_cols = [
        find_col(results_stream, "Assessment", "Score").unwrap(),
        find_col(results_stream, "Project", "Score").unwrap(),
    ]

    results = results_stream.as_ref()
    update_cols = [col for col in results.columns if col.find(RESULT_UPDATE) != -1]
    score_cols.extend(update_cols)
    scores = results[score_cols]
    new_scores: tuple[float, ...] = scores.sum().row(0)
    scores = pl.Series([score if score <= 100 else 100 for score in new_scores])
    results = results.with_columns(
        pl.Series("New Score", scores).alias(det_result_col())
    )
    return Result.ok(DataStream(results))
