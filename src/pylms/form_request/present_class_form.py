from ..constants import COHORT, NAME
from ..data import DataStore
from ..errors import Result, eprint
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
    run_share_form,
)


def init_present_form(ds: DataStore, input_date: str, email: str) -> Result[Form]:
    names: list[str] = ds.pretty()[NAME].tolist()
    cohort_no: int = ds.as_ref()[COHORT].iloc[0]
    head = return_name(cohort_no, "Attendance", input_date)
    form_title, form_name = head.title, head.name
    present_form: Form | None = run_create_form(form_title, form_name)
    if present_form is None:
        msg = f"Form creation failed when creating attendance for students for date {input_date}. \nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)

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
    present_form = run_setup_form(
        present_form,
        form_content,
    )
    if present_form is None:
        msg = f"Form setup failed when creating attendance for students for date {input_date}. \nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)

    present_form = run_publish_form(present_form)

    if present_form is None:
        msg = "Failed to publish form. Please try again."
        eprint(msg)
        return Result.err(msg)

    present_form = run_share_form(present_form, email)
    if present_form is None:
        msg = "Form sharing failed when trying to share form \nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)

    return Result.ok(present_form)
