import pandas as pd

from ..data import DataStream
from ..errors import Result
from ..models import ClassFormInfo
from ..paths_class import get_class_path
from .enums import ClassType
from .form import retrieve_form


def retrieve_class_form(
    class_date: str, class_type: ClassType
) -> Result[DataStream[pd.DataFrame]]:
    class_path = get_class_path(class_date, "class")
    if class_path.is_err():
        return class_path.propagate()

    class_path = class_path.unwrap()

    record_path = get_class_path(class_date, "record")
    if record_path.is_err():
        return record_path.propagate()

    record_path = record_path.unwrap()

    return retrieve_form(class_path, record_path, ClassFormInfo, class_type=class_type)
