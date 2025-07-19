from datetime import datetime

from pylms.constants import COHORT, DATE_FMT, FORM_DATE_FMT, NAME
from pylms.forms.request_form_api.errors import FormServiceError
from pylms.forms.utils import (
    create_form,
    setup_form,
    share_form,
)
from pylms.models import (
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
    TextQuestion,
)
from pylms.utils import DataStore


def init_excused_form(ds: DataStore, input_date: str, email: str) -> Form:
    names: list[str] = ds.pretty()[NAME].tolist()
    cohort_no: int = ds()[COHORT].iloc[0]
    title_date: str = datetime.strptime(input_date, DATE_FMT).strftime(FORM_DATE_FMT)
    form_title: str = (
        f"Python Beginners Cohort {cohort_no} Excused List for {input_date}"
    )
    form_name: str = f"Excused {title_date}"
    excused_form: Form | None = create_form(form_title, form_name)
    if excused_form is None:
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
            Content(
                createItem=CreateItem(
                    item=Item(
                        title="Reason",
                        questionItem=QuestionItem(
                            question=Question(
                                required=True, textQuestion=TextQuestion(paragraph=True)
                            )
                        ),
                    ),
                    location=Location(index=2),
                )
            ),
        ]
    )
    excused_form = setup_form(
        excused_form,
        form_content,
    )
    if excused_form is None:
        raise FormServiceError(
            "setup",
            f"Form creation failed when creating excused list for students for date {input_date}. \nPlease restart the program and try again.",
        )

    excused_form = share_form(excused_form, email)
    if excused_form is None:
        raise FormServiceError(
            "share",
            "Form sharing failed when trying to share form \nPlease restart the program and try again.",
        )
    return excused_form
