import re

import pandas as pd

from typing import cast

from pylms.forms.request_form_api import UpdateFormInfo
from pylms.forms.retrieve_form_api.form import retrieve_form
from pylms.forms.utils import select_form
from pylms.history import History
from pylms.utils import DataStream, paths


def _rename_date_col(col: str) -> str:
    if col.startswith("Class"):
        date_match: re.Match | None = re.search(r"\d{2}/\d{2}/\d{4}", col)
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
) -> tuple[DataStream[pd.DataFrame] | None, UpdateFormInfo]:
    info: UpdateFormInfo = cast(UpdateFormInfo, select_form(history, "update"))
    update_form_path, update_record_path = paths.ret_update_path(info.timestamp)
    result: DataStream[pd.DataFrame] | None = retrieve_form(
        update_form_path, update_record_path, UpdateFormInfo
    )
    if result is None:
        return None, info
    result = rename_date_col(result)
    return result, info
