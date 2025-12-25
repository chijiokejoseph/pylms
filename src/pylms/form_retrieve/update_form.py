import re

import pandas as pd

from ..data import DataStream
from ..errors import Result
from ..form_utils import UpdateFormInfo, select_form
from ..history import History
from .form import retrieve_form


def _rename_date_col(col: str) -> str:
    if col.startswith("Class"):
        date_match: re.Match[str] | None = re.search(r"\d{2}/\d{2}/\d{4}", col)
        if date_match is not None:
            return date_match.group()
        return col
    return col


def rename_date_col(data_stream: DataStream[pd.DataFrame]) -> DataStream[pd.DataFrame]:
    data: pd.DataFrame = data_stream()
    for column in data.columns:
        new_column = _rename_date_col(column)
        if new_column != column:
            data[new_column] = data[column]
            data = data.drop(columns=[column])

    return DataStream(data)


def retrieve_update_form(
    history: History,
) -> Result[tuple[DataStream[pd.DataFrame], UpdateFormInfo]]:
    info = select_form(history, "update")
    if info.is_err():
        return info.propagate()

    info = info.unwrap()

    result = retrieve_form(info)
    if result.is_err():
        return result.propagate()
    result = result.unwrap()

    result = rename_date_col(result)
    return Result.ok((result, info))
