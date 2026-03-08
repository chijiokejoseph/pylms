from ..constants import COHORT, NAME
from ..data import DataStore
from ..errors import Result
from ..form_utils import return_name
from ..models import (
    ChoiceQuestion,
    Content,
    ContentBody,
    CreateItem,
    Form,
    Item,
    Location,
    OptionDict,
    Question,
    QuestionItem,
)
from ..service import (
    run_create_form,
    run_publish_form,
    run_setup_form,
    run_share_form_multiple,
)


def init_present_form(ds: DataStore, input_date: str, gmails: list[str]) -> Result[Form]:
    """Initialize present attendance form for a specific date.
    
    Args:
        ds: DataStore containing student data.
        input_date: Date for the attendance form.
        gmails: List of Gmail addresses to share the form with.
        
    Returns:
        Result[Form]: Success with created form or error message.
    """
    # Extract student data
    pretty = ds.pretty()
    names: list[str] = pretty[NAME].to_list()
    cohort_no: int = pretty[0, COHORT]
    head = return_name(cohort_no, "Attendance", input_date)
    form_title, form_name = head.title, head.name
    
    # Create form
    present_form_result = run_create_form(form_title, form_name)
    if present_form_result.is_err():
        return present_form_result.propagate()
    present_form = present_form_result.unwrap()

    # Setup form content with name dropdown and date selection
    form_content: ContentBody = ContentBody(
        requests=[
            Content(
                createItem=CreateItem(
                    item=Item(
                        title=NAME,
                        questionItem=QuestionItem(
                            question=Question(
                                choiceQuestion=ChoiceQuestion(
                                    type="DROP_DOWN",
                                    options=[OptionDict(value=name) for name in names],
                                    shuffle=False,
                                ),
                                required=True,
                            )
                        ),
                    ),
                    location=Location(index=0),
                )
            ),
            Content(
                createItem=CreateItem(
                    item=Item(
                        title="Date",
                        questionItem=QuestionItem(
                            question=Question(
                                required=True,
                                choiceQuestion=ChoiceQuestion(
                                    type="RADIO",
                                    options=[OptionDict(value=input_date)],
                                    shuffle=False,
                                ),
                            )
                        ),
                    ),
                    location=Location(index=1),
                )
            ),
        ]
    )
    
    # Setup and publish form
    present_form_result = run_setup_form(present_form, form_content)
    if present_form_result.is_err():
        return present_form_result.propagate()
    present_form = present_form_result.unwrap()

    present_form_result = run_publish_form(present_form)
    if present_form_result.is_err():
        return present_form_result.propagate()
    present_form = present_form_result.unwrap()

    # Share form with admin and selected facilitators
    result = run_share_form_multiple(present_form, gmails)
    if result.is_err():
        return result.propagate()

    return Result.ok(present_form)
