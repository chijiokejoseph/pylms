import json
from pathlib import Path
from typing import Type

import pandas as pd

from pylms.constants import TIME, TIME_FMT
from pylms.forms.request_form_api import CDSFormInfo, ClassFormInfo, UpdateFormInfo
from pylms.forms.retrieve_form_api._data_form_response import ResponseModel
from pylms.forms.retrieve_form_api.enums import ClassType
from pylms.forms.utils.service import FormResource, ResponseResource, init_service
from pylms.utils import DataStream, date


@init_service("forms", "v1")
def retrieve_form_responses(
    question_id_map: dict[str, str],
    form_path: Path,
    cls: Type,
    class_type: ClassType | None = None,
    *,
    service: FormResource,
) -> DataStream[pd.DataFrame]:
    with open(form_path, "r", encoding="utf-8") as json_form:
        data = json.load(json_form)
        form_info: CDSFormInfo | ClassFormInfo | UpdateFormInfo = cls(**data)
        resource: FormResource = service.forms()
        response_resource: ResponseResource = resource.responses()
        match form_info:
            case _ if isinstance(
                form_info, ClassFormInfo
            ) and class_type == ClassType.PRESENT:
                request = response_resource.list(formId=form_info.present_id)
            case _ if isinstance(
                form_info, ClassFormInfo
            ) and class_type == ClassType.EXCUSED:
                request = response_resource.list(formId=form_info.excused_id)
            case _ if not isinstance(form_info, ClassFormInfo):
                request = response_resource.list(formId=form_info.uuid)

        response_dict: dict = request.execute()
        response_model: ResponseModel = ResponseModel(**response_dict)

    response_data_dict: dict[str, list[str]] = {
        column: [] for _, column in question_id_map.items()
    }
    response_data_dict.update({TIME: []})

    if response_model.responses is None:
        response_model.responses = []

    for form_response in response_model.responses:
        timestamp: str = form_response.lastSubmittedTime
        timestamp = date.parse(timestamp, dayfirst=True).strftime(TIME_FMT)
        response_data_dict[TIME].append(f"{timestamp}")

        for question_id, column in question_id_map.items():
            answer_model = form_response.answers[question_id]
            text_answer = answer_model.textAnswers
            answers = text_answer.answers
            assert (
                len(answers) == 1
            ), f"length of answers expected is 1, actual: {len(answers)}"
            answer: str = answers[0].value
            response_data_dict[column].append(answer)

    new_data: pd.DataFrame = pd.DataFrame(data=response_data_dict)
    return DataStream(new_data)
