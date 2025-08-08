import json
from pathlib import Path
from typing import Type, cast

from pylms.models import CDSFormInfo, ClassFormInfo, UpdateFormInfo
from pylms.models import FormModel
from pylms.forms.retrieve_form_api.enums import ClassType
from pylms.forms.utils.service import FormResource, run_service
from pylms.forms.retrieve_form_api.errors import InvalidRetrieveArgsError


def _retrieve_form_questions(
    form_path: Path,
    cls: Type,
    class_type: ClassType | None = None,
    *,
    service: FormResource,
) -> dict[str, str]:
    """
    Retrieves form questions from a form whose details are stored at the specified form path.

    :param form_path: (Path) - The path to a JSON file that holds the form's details.
    :type form_path: Path
    :param cls: (Type) - The class type used to instantiate the form data.
    :type cls: Type
    :param class_type: (ClassType | None) - The class type indicating the form type.
    :type class_type: ClassType | None
    :param service: (FormResource) - The FormResource object used to make API calls.
    :type service: FormResource

    :return: (dict[str, str]) - A dictionary mapping question IDs to their titles.
    :rtype: dict[str, str]
    """
    # open the form info file and load its data
    with open(form_path, "r", encoding="utf-8") as file:
        data: dict = json.load(file)

        # create an instance of the form class from the data
        form_info: CDSFormInfo | UpdateFormInfo | ClassFormInfo = cls(**data)

        # get the form resource
        resource: FormResource = service.forms()

        # get the form response based on the form info
        match form_info:
            case _ if (
                isinstance(form_info, ClassFormInfo) and class_type == ClassType.PRESENT
            ):
                form_response: dict = resource.get(
                    formId=form_info.present_id
                ).execute()
            case _ if (
                isinstance(form_info, ClassFormInfo) and class_type == ClassType.EXCUSED
            ):
                form_response = resource.get(formId=form_info.excused_id).execute()
            case _ if not isinstance(form_info, ClassFormInfo):
                form_response = resource.get(formId=form_info.uuid).execute()
            case _:
                raise InvalidRetrieveArgsError("")

        # create an instance of the form model from the form response
        form_model: FormModel = FormModel(**form_response)

    # create a dictionary mapping question IDs to their titles
    question_id_dict: dict[str, str] = {
        form_item.questionItem.question.questionId: form_item.title
        for form_item in form_model.items
    }
    return question_id_dict


def retrieve_form_questions(
    form_path: Path,
    cls: Type,
    class_type: ClassType | None = None,
) -> dict[str, str]:
    """
    Retrieves form questions from a form whose details are stored at the specified form path.

    :param form_path: (Path) - The path to a JSON file that holds the form's details.
    :type form_path: Path
    :param cls: (Type) - The class type used to instantiate the form data.
    :type cls: Type
    :param class_type: (ClassType | None) - The class type indicating the form type.
    :type class_type: ClassType | None

    :return: (dict[str, str]) - A dictionary mapping question IDs to their titles.
    :rtype: dict[str, str]
    """
    return run_service(
        "forms",
        "v1",
        lambda service: _retrieve_form_questions(
            form_path, cls, class_type, service=cast(FormResource, service)
        ),
    )
