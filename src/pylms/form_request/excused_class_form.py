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
    TextQuestion,
)
from ..service import (
    run_create_form,
    run_publish_form,
    run_setup_form,
    run_share_form,
)


def init_excused_form(ds: DataStore, input_date: str, email: str) -> Result[Form]:
    names: list[str] = ds.to_pretty()[NAME].tolist()
    cohort_no: int = ds.as_ref()[COHORT].iloc[0]
    head = return_name(cohort_no, "Excused", input_date)
    form_title, form_name = head.title, head.name
    excused_form: Form | None = run_create_form(form_title, form_name)
    if excused_form is None:
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
    excused_form = run_setup_form(
        excused_form,
        form_content,
    )
    if excused_form is None:
        msg = f"Form creation failed when creating attendance for students for date {input_date}. \nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)

    excused_form = run_publish_form(excused_form)

    if excused_form is None:
        msg = "Failed to publish form. Please try again."
        eprint(msg)
        return Result.err(msg)

    excused_form = run_share_form(excused_form, email)
    if excused_form is None:
        msg = "Form sharing failed when trying to share form \nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)
    return Result.ok(excused_form)
