from typing import NamedTuple, cast
import numpy as np

from pylms.constants import DATA_COLUMNS
from pylms.utils.data import DataStream
from pylms.utils.paths import get_paths_excel
import pandas as pd


class Percents(NamedTuple):
    attendance: float
    assessment: float
    project: float


def collate_grade(
    data_stream: DataStream[pd.DataFrame], percents: Percents
) -> DataStream[pd.DataFrame]:
    total: float = sum(percents)
    if total != 1:
        raise ValueError("argument passed to percents must sum to 1.")

    required_cols: list[str] = [
        f"Attendance {percents.attendance * 100:.2f}%",
        f"Assessment {percents.assessment * 100:.2f}%",
        f"Project {percents.project * 100:.2f}%",
    ]
    cols_array: np.ndarray = np.array(required_cols)

    idx_array: np.ndarray = np.array([abs(item) > 1e-3 for item in percents])
    cols_array = cols_array[idx_array]

    def validator(test_data: pd.DataFrame) -> bool:
        for col in cols_array:
            if col not in test_data.columns.tolist():
                return False
        return True

    data_stream = DataStream(data_stream(), validator)
    temp = data_stream().loc[:, cols_array.tolist()]
    grade_data: pd.DataFrame = cast(pd.DataFrame, temp)
    total_data: pd.Series = grade_data.sum(axis=1)
    pass_idx: pd.Series = total_data >= 50
    remark: list[str] = ["Pass" if passed else "Fail" for passed in pass_idx.tolist()]
    old_data: pd.DataFrame = data_stream()
    old_data["Total 100%"] = total_data
    old_data["Pass"] = remark
    result_ds: DataStream[pd.DataFrame] = DataStream(old_data)
    result_ds.to_excel(get_paths_excel()["Result"])
    student_data: pd.DataFrame = data_stream()[DATA_COLUMNS]
    passed_data = student_data.loc[pass_idx]
    return DataStream(passed_data)
