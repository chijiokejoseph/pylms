from pathlib import Path

import pandas as pd

from pylms.forms.request_form_api import ClassFormInfo
from pylms.forms.retrieve_form_api.enums import ClassType
from pylms.forms.retrieve_form_api.form import retrieve_form
from pylms.utils import DataStream, paths


def retrieve_class_form(
    class_date: str, class_type: ClassType
) -> DataStream[pd.DataFrame] | None:
    class_path: Path = paths.get_class_path(class_date, "class")
    record_path: Path = paths.get_class_path(class_date, "record")
    return retrieve_form(class_path, record_path, ClassFormInfo, class_type=class_type)
