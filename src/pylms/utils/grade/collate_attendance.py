from pylms.constants import DATA_COLUMNS
from pylms.utils.data import DataStore, DataStream
import pandas as pd


def collate_attendance(
    ds: DataStore,
    percent: float,
    excluded_cols: list[str] | None = None,
) -> DataStream[pd.DataFrame]:
    if excluded_cols is None:
        excluded_cols = []
    filtered_data: pd.DataFrame = ds().drop(columns=excluded_cols)
    filtered_data = filtered_data.drop(columns=DATA_COLUMNS)
    scores: list[float] = []
    for row, row_series in filtered_data.iterrows():
        count: int = 0
        for item in row_series.tolist():
            if item == "Present" or item == "Excused":
                count += 1
        score: float = count * 100 / filtered_data.shape[1]
        score = score * percent
        score = round(score, 2)
        scores.append(score)
    old_data: pd.DataFrame = ds().loc[:, DATA_COLUMNS]
    column_name: str = f"Attendance {percent * 100:.2f}%"
    old_data[column_name] = scores
    return DataStream(old_data)
