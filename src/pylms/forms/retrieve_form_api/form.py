from pathlib import Path
from typing import Type

import pandas as pd
from google.auth.exceptions import TransportError
from googleapiclient.http import HttpError

from pylms.constants import NAME
from pylms.forms.retrieve_form_api.enums import ClassType
from pylms.forms.retrieve_form_api.errors import NetworkError
from pylms.forms.retrieve_form_api.form_questions import (
    retrieve_form_questions,
)
from pylms.forms.retrieve_form_api.form_responses import (
    retrieve_form_responses,
)
from pylms.utils import DataStream, clean_special


def retrieve_form(
    form_path: Path, record_path: Path, cls: Type, class_type: ClassType | None = None
) -> DataStream[pd.DataFrame] | None:
    if not form_path.exists():
        print(
            f"No record of an existing form found. \nBecause expected data form metadata file '{form_path.name}' which is supposed to be located at \n{form_path} is not found."
        )
        return None
    if record_path.exists():
        print(
            f"{form_path.name} and {record_path.name} exist, \nshowing that the information stored in the form with metadata file {form_path.name} has been recorded. \nHence no further retrieval is necessary."
        )
        return None
    try:
        questions_id_to_columns: dict[str, str] = retrieve_form_questions(
            form_path, cls=cls, class_type=class_type
        )
    except (HttpError, TransportError) as e:
        raise NetworkError(str(e))

    try:
        result: DataStream[pd.DataFrame] = retrieve_form_responses(
            questions_id_to_columns, form_path, cls=cls, class_type=class_type
        )
    except (HttpError, TransportError) as e:
        raise NetworkError(str(e))

    result = clean_special.clean_duplicates(result, [NAME])
    return result
