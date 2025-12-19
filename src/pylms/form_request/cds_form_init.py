import json
from datetime import datetime
from pathlib import Path

import pandas as pd

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
from ..paths import get_cds_path
from ..service import (
    run_create_form,
    run_publish_form,
    run_setup_form,
    run_share_form,
)


def init_cds_form(ds: DataStore, history: History) -> Result[Unit]:
    data: pd.DataFrame = ds.pretty()
    nysc_selector: pd.Series = data[INTERNSHIP] == "NYSC"
    corpers: pd.Series = data[NAME].loc[nysc_selector]
    corper_names: list[str] = corpers.tolist()
    cohort_no: int = data[COHORT].iloc[0]
    timestamp: str = datetime.now().strftime(TIMESTAMP_FMT)

    head = return_name(cohort_no, "CDS")
    form_title, form_name = head.title, head.name

    cds_form: Form | None = run_create_form(form_title, form_name)

    if cds_form is None:
        msg = f"Form creation failed when creating CDS Entry Forms for students for cohort {cohort_no}. \n\nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)

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

    email_result = input_email(
        "Enter an email address to share the form with: ",
    )
    if email_result.is_err():
        return email_result.propagate()
    recipient_email: str = email_result.unwrap()
    cds_form = run_share_form(cds_form, recipient_email)
    if cds_form is None:
        msg = f"Form sharing failed when sharing the form with {recipient_email}. \n\nPlease restart the program and try again."
        eprint(msg)
        return Result.err(msg)

    info: CDSFormInfo = CDSFormInfo(
        name=cds_form.name,
        title=cds_form.title,
        url=cds_form.url,
        uuid=cds_form.uuid,
        timestamp=timestamp,
    )
    add_cds_form(history, info)
    cds_form_path: Path = get_cds_path("form", info.timestamp)
    with open(cds_form_path, "w") as json_file:
        json.dump(info.model_dump(), json_file, indent=2)

    return Result.unit()
