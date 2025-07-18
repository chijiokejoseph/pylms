from datetime import datetime

from pylms.constants import COHORT, DATE_FMT, FORM_DATE_FMT, NAME
from pylms.forms.request_form_api.errors import FormServiceError
from pylms.forms.utils.service import (
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
    create_form,
    setup_form,
    share_form,
)
from pylms.utils import DataStore


def init_present_form(ds: DataStore, input_date: str, email: str) -> Form:
    names: list[str] = ds.pretty()[NAME].tolist()
    cohort_no: int = ds()[COHORT].iloc[0]
    title_date: str = datetime.strptime(input_date, DATE_FMT).strftime(FORM_DATE_FMT)
    form_title: str = f"Python Beginners Cohort {cohort_no} Attendance for {input_date}"
    form_name: str = f"Attendance {title_date}"
    present_form: Form | None = create_form(form_title, form_name)
    if present_form is None:
        raise FormServiceError(
            "create",
            f"Form creation failed when creating attendance for students for date {input_date}. \nPlease restart the program and try again.",
        )

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
    present_form = setup_form(
        present_form,
        form_content,
    )
    if present_form is None:
        raise FormServiceError(
            "setup",
            f"Form setup failed when creating attendance for students for date {input_date}. \nPlease restart the program and try again.",
        )
    present_form = share_form(present_form, email)
    if present_form is None:
        raise FormServiceError(
            "share",
            "Form sharing failed when trying to share form \nPlease restart the program and try again.",
        )

    return present_form
