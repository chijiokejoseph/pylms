from datetime import datetime

import polars as pl

from ..config import Config
from ..constants import CDS, COHORT, INTERNSHIP, NAME, TIMESTAMP_FMT, WORK_DAYS
from ..data import DataStore
from ..errors import Result, Unit
from ..form_utils import return_name
from ..history import History, add_cds_form
from ..models import (
    CDSFormInfo,
    ChoiceQuestion,
    Content,
    ContentBody,
    CreateItem,
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
from .share_emails import input_share_emails


def init_cds_form(config: Config, ds: DataStore, history: History) -> Result[Unit]:
    """Initialize and create CDS form for NYSC corpers.

    Args:
        config: Config containing admin and facilitator information.
        ds: DataStore containing student data.
        history: History object for tracking operations.

    Returns:
        Result[Unit]: Success or error message.
    """
    pretty = ds.pretty()
    # Filter for NYSC corpers only
    corpers = pretty.filter(pl.col(INTERNSHIP) == "NYSC")
    corper_names: list[str] = corpers[NAME].to_list()
    cohort_no: int = pretty[0, COHORT]
    timestamp: str = datetime.now().strftime(TIMESTAMP_FMT)

    # Create form with CDS title
    head = return_name(cohort_no, "CDS")
    form_title, form_name = head.title, head.name

    form_result = run_create_form(form_title, form_name)
    if form_result.is_err():
        return form_result.propagate()
    form = form_result.unwrap()

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
    form_result = run_setup_form(form, cds_content)
    if form_result.is_err():
        return form_result.propagate()
    form = form_result.unwrap()

    form_result = run_publish_form(form)
    if form_result.is_err():
        return form_result.propagate()
    form = form_result.unwrap()

    # Get emails to share with
    gmails_result = input_share_emails(config)
    if gmails_result.is_err():
        return gmails_result.propagate()
    gmails = gmails_result.unwrap()

    # Share form with admin and selected facilitators
    form_result = run_share_form_multiple(form, gmails)
    if form_result.is_err():
        return form_result.propagate()
    form = form_result.unwrap()

    # Save form info to history
    info: CDSFormInfo = CDSFormInfo(
        name=form.name,
        title=form.title,
        url=form.url,
        uuid=form.uuid,
        timestamp=timestamp,
    )
    add_cds_form(history, info)

    return Result.unit()
