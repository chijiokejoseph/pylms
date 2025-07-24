import re

import pandas as pd

from pylms.constants import COMPLETION, DATA_COLUMNS
from pylms.utils.data import DataStream


def preprocess_col(col: str) -> str:
    match str(col):
        case _ if re.match(r"nysc\s*/\s*siwes", col, flags=re.IGNORECASE):
            return COMPLETION
        case _:
            return col.strip().title()


def clean_columns(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    data: pd.DataFrame = data_stream()
    columns: list[str] = data.columns.tolist()
    col_mappings: dict[str, str] = {preprocess_col(col): col for col in columns}
    data = data.rename(columns=col_mappings)
    print(f"{data.columns.tolist() = }")
    columns_to_drop: list[str] = [col for col in columns if col not in DATA_COLUMNS]
    data = data.drop(columns=columns_to_drop)
    return DataStream(data)
