import json
from pathlib import Path
from typing import Type, cast

import pandas as pd

from pylms.constants import TIME, TIME_FMT
from pylms.models import CDSFormInfo, ClassFormInfo, UpdateFormInfo, ResponseModel
from pylms.forms.retrieve_form_api.enums import ClassType
from pylms.forms.utils.service import FormResource, ResponseResource, run_service
from pylms.utils import DataStream, date
from pylms.forms.retrieve_form_api.errors import InvalidRetrieveArgsError


def _retrieve_form_responses(
    question_id_map: dict[str, str],
    form_path: Path,
    cls: Type,
    class_type: ClassType | None = None,
    *,
    service: FormResource,
) -> DataStream[pd.DataFrame]:
    """
    Retrieves form responses from a form whose details are stored at the specified form path.

    :param question_id_map: A dictionary mapping question IDs to the column names
        in the output DataFrame.
    :type question_id_map: dict[str, str]
    :param form_path: The path to a JSON file that holds the form's details.
    :type form_path: Path
    :param cls: The class type used to instantiate the form data.
    :type cls: Type
    :param class_type: The class type indicating the form type.
    :type class_type: ClassType | None
    :param service: The FormResource object used to make API calls.
    :type service: FormResource

    :return: A DataStream that yields a DataFrame with the form responses.
    :rtype: DataStream[pd.DataFrame]
    """
    # open the form info file and load its data
    with open(form_path, "r", encoding="utf-8") as json_form:
        data = json.load(json_form)
        
        # create an instance of the form class from the data
        form_info: CDSFormInfo | ClassFormInfo | UpdateFormInfo = cls(**data)
        
        # get the form resource
        resource: FormResource = service.forms()
        
        # get the response resource
        response_resource: ResponseResource = resource.responses()
        
        # determine which form to retrieve responses from based on the class type
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
                request = response_resource.list(formId=form_info.timestamp)
            case _:
                raise InvalidRetrieveArgsError("")
            
        # execute the request and load its response
        response_dict: dict = request.execute()
        response_model: ResponseModel = ResponseModel(**response_dict)

    # create a dictionary with the column names and an empty list for each
    response_data_dict: dict[str, list[str]] = {
        column: [] for _, column in question_id_map.items()
    }
    
    # add a key for the timestamp column
    response_data_dict.update({TIME: []})

    # if there are no responses, 
    # set the `responses` field to an empty list
    if response_model.responses is None:
        response_model.responses = []

    # iterate over each form response
    for form_response in response_model.responses:
        
        # get the timestamp of the form response
        timestamp: str = form_response.lastSubmittedTime
        
        # parse the timestamp using the date library
        parsed_timestamp = date.parse(timestamp, dayfirst=True)
        
        # format the parsed timestamp as a string
        timestamp_str = parsed_timestamp.strftime(TIME_FMT)
        
        # append the timestamp to the response data dictionary
        response_data_dict[TIME].append(f"{timestamp_str}")

        # iterate over each question and its column name
        for question_id, column in question_id_map.items():
            
            # get the answer model for the question
            answer_model = form_response.answers[question_id]
            
            # get the text answers for the question
            text_answer = answer_model.textAnswers
            
            # get the list of answers
            answers = text_answer.answers
            
            # assert that there is only one answer
            assert len(answers) == 1, (
                f"length of answers expected is 1, actual: {len(answers)}"
            )
            
            # get the answer
            answer: str = answers[0].value
            
            # append the answer to the response data dictionary
            response_data_dict[column].append(answer)

    # create a DataFrame from the response data dictionary
    new_data: pd.DataFrame = pd.DataFrame(data=response_data_dict)
    
    # return a DataStream that yields the DataFrame
    return DataStream(new_data)


def retrieve_form_responses(
    question_id_map: dict[str, str], form_path: Path, cls: Type, class_type: ClassType | None
) -> DataStream[pd.DataFrame]:
    """
    Retrieves responses to a form.

    :param question_id_map: (dict[str, str]) - A dictionary mapping question IDs to the column names
        in the output DataFrame.
    :type question_id_map: dict[str, str]
    :param form_path: (Path) - The path to a JSON file containing the form's information.
    :type form_path: Path
    :param cls: (Type) - The class type used to instantiate the form information.
    :type cls: Type
    :param class_type - (ClassType | None): The class type of the form.
    :type class_type: ClassType | None

    :return: (DataStream[pd.DataFrame]) - A DataStream that yields a DataFrame with the form responses.
    :rtype: DataStream[pd.DataFrame]
    """
    return run_service(
        "forms",
        "v1",
        lambda service: _retrieve_form_responses(
            question_id_map, form_path, cls, class_type, service=cast(FormResource, service)
        ),
    )
