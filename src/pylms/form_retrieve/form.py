import pandas as pd
from google.auth.exceptions import TransportError
from googleapiclient.http import HttpError  # pyright: ignore [reportMissingTypeStubs]

from pylms.models import AllFormInfo

from ..clean import clean_duplicates_with_cols
from ..constants import NAME
from ..data import DataStream
from ..errors import Result, eprint
from .enums import ClassType
from .form_questions import (
    retrieve_form_questions,
)
from .form_responses import (
    retrieve_form_responses,
)


def retrieve_form(
    info: AllFormInfo,
    class_type: ClassType | None = None,
) -> Result[DataStream[pd.DataFrame]]:
    """
    Retrieves a form and its responses from Google Forms.

    :param form_path: (Path) - The path to a JSON file that holds the form's details.
    :type form_path: Path
    :param record_path: (Path) - The path to a JSON file that holds the form's responses.
    :type record_path: Path
    :param cls: (Type) - The class type used to instantiate the form data.
    :type cls: Type
    :param class_type: (ClassType | None) - The class type indicating the form type.
    :type class_type: ClassType | None

    :return: (DataStream[pd.DataFrame] | None) - A DataStream that yields a DataFrame with the form responses.
    :rtype: DataStream[pd.DataFrame] | None
    """

    try:
        questions_id_to_columns = retrieve_form_questions(info, class_type=class_type)
        if questions_id_to_columns.is_err():
            return questions_id_to_columns.propagate()

        questions_id_to_columns = questions_id_to_columns.unwrap()
    except (HttpError, TransportError) as e:
        msg = f"Retrieval failed due to connection issues.\nError: {e}"
        eprint(msg)
        return Result.err(msg)

    try:
        result = retrieve_form_responses(
            questions_id_to_columns, info, class_type=class_type
        )
        if result.is_err():
            return result.propagate()

        result = result.unwrap()
    except (HttpError, TransportError) as e:
        msg = f"Retrieval failed due to connection issues.\nError: {e}"
        eprint(msg)
        return Result.err(msg)

    result = clean_duplicates_with_cols(result, [NAME])
    return Result.ok(result)
