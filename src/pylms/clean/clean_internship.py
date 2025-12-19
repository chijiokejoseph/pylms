import pandas as pd

from ..constants import INTERNSHIP
from ..data import DataStream


def clean_internship(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    data: pd.DataFrame = data_stream()

    data[INTERNSHIP] = data[INTERNSHIP].apply(str.upper)  # pyright: ignore [reportUnknownMemberType]

    def validate(test_data: pd.DataFrame) -> bool:
        test1: bool = INTERNSHIP in test_data.columns.tolist()
        internship_col: list[str] = test_data[INTERNSHIP].tolist()
        test2: bool = all([row.isupper() for row in internship_col])
        return test1 and test2

    return DataStream(data, validate)
