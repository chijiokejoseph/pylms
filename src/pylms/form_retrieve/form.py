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
) -> Result[DataStream]:
    """Retrieve form and its responses from Google Forms.
    
    Fetches form questions and responses, then cleans duplicates based on name.
    
    Args:
        info (AllFormInfo): Form information containing IDs and details.
        class_type (ClassType | None): Type of class form (present/excused) if applicable.
        
    Returns:
        Result[DataStream]: Success with form response data or error message.
    """
    try:
        # Retrieve form questions mapping
        questions_id_to_columns = retrieve_form_questions(info, class_type=class_type)
        if questions_id_to_columns.is_err():
            return questions_id_to_columns.propagate()

        questions_id_to_columns = questions_id_to_columns.unwrap()
    except (HttpError, TransportError) as e:
        msg = f"Retrieval failed due to connection issues.\nError: {e}"
        eprint(msg)
        return Result.err(msg)

    try:
        # Retrieve form responses
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

    # Clean duplicates based on name column
    result = clean_duplicates_with_cols(result.as_ref(), [NAME])
    return Result.ok(DataStream(result))
