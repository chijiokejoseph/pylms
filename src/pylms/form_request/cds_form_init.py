from datetime import datetime

import polars as pl

from ..cli import input_email
from ..constants import CDS, COHORT, INTERNSHIP, NAME, TIMESTAMP_FMT, WORK_DAYS
from ..data import DataStore
from ..errors import Result, Unit, eprint
from ..form_utils import return_name
from ..history import History, add_cds_form
from ..models import (
    CDSFormInfo,
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


def init_cds_form(ds: DataStore, history: History) -> Result[Unit]:
    """Initialize and create CDS form for NYSC corpers.
    
    Args:
        ds (DataStore): DataStore containing student data.
        history (History): History object for tracking operations.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    pretty = ds.pretty()
    # Filter for NYSC corpers only
    corpers = pretty.filter(pl.col(INTERNSHIP) == "NYSC")
    corper_names: list[str] = corpers[NAME].to_list()  # Fixed: should be NAME not INTERNSHIP
    cohort_no: int = pretty[0, COHORT]
    timestamp: str = datetime.now().strftime(TIMESTAMP_FMT)

    # Create form with CDS title
    head = return_name(cohort_no, "CDS")
    form_title, form_name = head.title, head.name

    cds_form: Form | None = run_create_form(form_title, form_name)

    if cds_form is None:
        msg = f"Form creation failed when creating CDS Entry Forms for students for cohort {cohort_no}. \n\nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)

    # Setup form content with name dropdown and CDS day selection
    cds_content: ContentBody = ContentBody(
        requests=[
            Content(
                createItem=CreateItem(
                    item=Item(
                        title=NAME,
                        description="Choose your name from the dropdown. Please note that the names displayed below are only for corpers i.e., those whose internships are NYSC.",
                        questionItem=QuestionItem(
                            question=Question(
                                choiceQuestion=ChoiceQuestion(
                                    type="DROP_DOWN",
                                    shuffle=False,
                                    options=[
                                        OptionDict(value=name) for name in corper_names
                                    ],
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
                        title=CDS,
                        description="Select your CDS Day",
                        questionItem=QuestionItem(
                            question=Question(
                                required=True,
                                choiceQuestion=ChoiceQuestion(
                                    type="RADIO",
                                    shuffle=False,
                                    options=[
                                        OptionDict(value=day) for day in WORK_DAYS
                                    ],
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
    cds_form = run_setup_form(cds_form, cds_content)
    if cds_form is None:
        msg = f"Form setup failed when setting up CDS Entry Forms for students for cohort {cohort_no}. \n\nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)

    cds_form = run_publish_form(cds_form)

    if cds_form is None:
        msg = "Failed to publish form. Please try again."
        eprint(msg)
        return Result.err(msg)

    # Share form with recipient
    recipient_email = input_email(
        "Enter an email address to share the form with: ",
    )
    if recipient_email.is_err():
        return recipient_email.propagate()
    recipient_email = recipient_email.unwrap()

    cds_form = run_share_form(cds_form, recipient_email)
    if cds_form is None:
        msg = f"Form sharing failed when sharing the form with {recipient_email}. \n\nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)

    # Save form info to history
    info: CDSFormInfo = CDSFormInfo(
        name=cds_form.name,
        title=cds_form.title,
        url=cds_form.url,
        uuid=cds_form.uuid,
        timestamp=timestamp,
    )
    add_cds_form(history, info)

    return Result.unit()
