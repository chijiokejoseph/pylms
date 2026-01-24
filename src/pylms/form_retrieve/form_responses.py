import polars as pl
from dateutil.parser import parse

from ..constants import TIME, TIME_FMT
from ..data import DataStream
from ..errors import Result, eprint
from ..models import (
    AllFormInfo,
    ClassFormInfo,
    Response,
    ResponseModel,
)
from ..service import FormsService, ResponseResource, run_service
from .enums import ClassType


def _retrieve_form_responses(
    question_id_map: dict[str, str],
    form_info: AllFormInfo,
    class_type: ClassType | None = None,
    *,
    service: FormsService,
) -> Result[DataStream]:
    """Retrieve form responses from Google Forms API.
    
    Args:
        question_id_map (dict[str, str]): Mapping of question IDs to column names.
        form_info (AllFormInfo): Form information containing IDs.
        class_type (ClassType | None): Type of class form if applicable.
        service (FormsService): Google Forms service instance.
        
    Returns:
        Result[DataStream]: Success with response data or error message.
    """
    # Get response resource
    response_resource: ResponseResource = service.forms().responses()

    # Determine which form to retrieve responses from
    match form_info:
        case _ if (
            isinstance(form_info, ClassFormInfo) and class_type == ClassType.PRESENT
        ):
            request = response_resource.list(formId=form_info.present_id)
        case _ if (
            isinstance(form_info, ClassFormInfo) and class_type == ClassType.EXCUSED
        ):
            request = response_resource.list(formId=form_info.excused_id)
        case _ if not isinstance(form_info, ClassFormInfo):
            request = response_resource.list(formId=form_info.uuid)
        case _:
            msg = f"specified form_info type {type(form_info).__name__} and class type {class_type} are invalid"
            eprint(msg)
            return Result.err(msg)

    # Execute request and load response
    response_dict: dict[str, list[Response]] = request.execute()  # pyright: ignore [reportUnknownMemberType]
    response_model: ResponseModel = ResponseModel(**response_dict)

    # Create dictionary with column names and empty lists
    response_data_dict: dict[str, list[str]] = {
        column: [] for _, column in question_id_map.items()
    }
    response_data_dict.update({TIME: []})

    # Handle case with no responses
    if response_model.responses is None:
        response_model.responses = []

    # Process each form response
    for form_response in response_model.responses:
        # Parse and format timestamp
        timestamp: str = form_response.lastSubmittedTime
        parsed_timestamp = parse(timestamp, dayfirst=True)
        timestamp_str = parsed_timestamp.strftime(TIME_FMT)
        response_data_dict[TIME].append(f"{timestamp_str}")

        # Process each question answer
        for question_id, column in question_id_map.items():
            answer_model = form_response.answers[question_id]
            text_answer = answer_model.textAnswers
            answers = text_answer.answers

            # Validate single answer per question
            if len(answers) != 1:
                msg = f"length of answers expected is 1, actual: {len(answers)}"
                eprint(msg)
                return Result.err(msg)

            answer: str = answers[0].value
            response_data_dict[column].append(answer)

    # Create DataFrame from response data
    new_data = pl.DataFrame(data=response_data_dict)
    return Result.ok(DataStream(new_data))


def retrieve_form_responses(
    question_id_map: dict[str, str],
    info: AllFormInfo,
    class_type: ClassType | None,
) -> Result[DataStream]:
    """Retrieve responses to a form using Google Forms service.
    
    Args:
        question_id_map (dict[str, str]): Mapping of question IDs to column names.
        info (AllFormInfo): Form information containing IDs.
        class_type (ClassType | None): Type of class form if applicable.
        
    Returns:
        Result[DataStream]: Success with form response data or error message.
    """
    def _run_service(service: FormsService) -> Result[DataStream]:
        return _retrieve_form_responses(
            question_id_map,
            info,
            class_type,
            service=service,
        )

    return run_service(
        "forms",
        "v1",
        _run_service,
    )
