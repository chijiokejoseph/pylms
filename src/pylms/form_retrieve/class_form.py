import pandas as pd

from pylms.history import History, match_info_by_date

from ..data import DataStream
from ..errors import Result
from .enums import ClassType
from .form import retrieve_form


def retrieve_class_form(
    history: History, class_date: str, class_type: ClassType
) -> Result[DataStream[pd.DataFrame]]:
    info = match_info_by_date(history, class_date)
    if info.is_err():
        return info.propagate()
    info = info.unwrap()

    return retrieve_form(info, class_type=class_type)
