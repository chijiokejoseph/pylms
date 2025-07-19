import json
from pathlib import Path
from typing import Type

from pylms.models import CDSFormInfo, ClassFormInfo, UpdateFormInfo
from pylms.models import FormModel
from pylms.forms.retrieve_form_api.enums import ClassType
from pylms.forms.utils.service import FormResource, init_service
from pylms.forms.retrieve_form_api.errors import InvalidRetrieveArgsError


@init_service("forms", "v1")
def retrieve_form_questions(
    form_path: Path,
    cls: Type,
    class_type: ClassType | None = None,
    *,
    service: FormResource,
) -> dict[str, str]:
    with open(form_path, "r", encoding="utf-8") as file:
        data: dict = json.load(file)
        form_info: CDSFormInfo | UpdateFormInfo | ClassFormInfo = cls(**data)
        resource: FormResource = service.forms()
        match form_info:
            case _ if isinstance(
                form_info, ClassFormInfo
            ) and class_type == ClassType.PRESENT:
                form_response: dict = resource.get(
                    formId=form_info.present_id
                ).execute()
            case _ if isinstance(
                form_info, ClassFormInfo
            ) and class_type == ClassType.EXCUSED:
                form_response = resource.get(formId=form_info.excused_id).execute()
            case _ if not isinstance(form_info, ClassFormInfo):
                form_response = resource.get(formId=form_info.uuid).execute()
            case _:
                raise InvalidRetrieveArgsError("")

        form_model: FormModel = FormModel(**form_response)

    question_id_dict: dict[str, str] = {
        form_item.questionItem.question.questionId: form_item.title
        for form_item in form_model.items
    }
    return question_id_dict
