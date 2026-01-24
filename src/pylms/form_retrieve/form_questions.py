from typing import Any

from ..errors import Result, eprint
from ..models import AllFormInfo, ClassFormInfo, FormModel
from ..service import FormResource, FormsService, run_service
from .enums import ClassType


def _retrieve_form_questions(
    info: AllFormInfo,
    class_type: ClassType | None = None,
    *,
    service: FormsService,
) -> Result[dict[str, str]]:
    """Retrieve form questions from Google Forms API.
    
    Args:
        info (AllFormInfo): Form information containing IDs.
        class_type (ClassType | None): Type of class form if applicable.
        service (FormsService): Google Forms service instance.
        
    Returns:
        Result[dict[str, str]]: Success with question ID to title mapping or error.
    """
    # Get form resource
    resource: FormResource = service.forms()

    # Get form response based on form info and class type
    match info:
        case _ if isinstance(info, ClassFormInfo) and class_type == ClassType.PRESENT:
            form_response: dict[Any, Any] = resource.get(  # pyright: ignore[reportUnknownMemberType]
                formId=info.present_id
            ).execute()
        case _ if isinstance(info, ClassFormInfo) and class_type == ClassType.EXCUSED:
            form_response = resource.get(formId=info.excused_id).execute()  # pyright: ignore[reportUnknownMemberType]
        case _ if not isinstance(info, ClassFormInfo):
            form_response = resource.get(formId=info.uuid).execute()  # pyright: ignore[reportUnknownMemberType]
        case _:
            msg = f"specified form_info type {type(info).__name__} and class type {class_type} are invalid"
            eprint(msg)
            return Result.err(msg)

    # Create form model from response
    form_model: FormModel = FormModel(**form_response)

    # Create mapping of question IDs to titles
    question_id_dict: dict[str, str] = {
        form_item.questionItem.question.questionId: form_item.title
        for form_item in form_model.items
    }
    return Result.ok(question_id_dict)


def retrieve_form_questions(
    info: AllFormInfo,
    class_type: ClassType | None = None,
) -> Result[dict[str, str]]:
    """Retrieve form questions using Google Forms service.
    
    Args:
        info (AllFormInfo): Form information containing IDs.
        class_type (ClassType | None): Type of class form if applicable.
        
    Returns:
        Result[dict[str, str]]: Success with question ID to title mapping or error.
    """
    def _run_service(service: FormsService) -> Result[dict[str, str]]:
        return _retrieve_form_questions(info, class_type, service=service)

    return run_service("forms", "v1", _run_service)
