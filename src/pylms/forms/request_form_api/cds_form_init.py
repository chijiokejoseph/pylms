import json
from io import TextIOWrapper
from pathlib import Path
from typing import cast
from datetime import datetime

import pandas as pd

from pylms.cli import input_email
from pylms.constants import CDS, COHORT, WORK_DAYS, INTERNSHIP, NAME
from pylms.forms.request_form_api.errors import FormServiceError
from pylms.forms.request_form_api.utils import CDSFormInfo
from pylms.forms.utils.service import (
    run_create_form,
    run_setup_form,
    run_share_form,
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
)
from pylms.utils import DataStore, paths
from pylms.constants import TIMESTAMP_FMT
from pylms.history import History


def init_cds_form(ds: DataStore, history: History) -> None:
    data: pd.DataFrame = ds.pretty()
    nysc_selector: pd.Series = data[INTERNSHIP] == "NYSC"
    corpers: pd.Series = data[NAME].loc[nysc_selector]
    corper_names: list[str] = corpers.tolist()
    cohort_no: int = data[COHORT].iloc[0]
    timestamp: str = datetime.now().strftime(TIMESTAMP_FMT)
    
    form_title: str = f"Python Beginners Cohort {cohort_no} CDS Entry Form"
    form_name: str = f"Cohort {cohort_no} CDS {timestamp}"
    
    cds_form: Form | None = run_create_form(form_title, form_name)

    if cds_form is None:
        raise FormServiceError(
            "create",
            f"Form creation failed when creating CDS Entry Forms for students for cohort {cohort_no}. \nPlease restart the program and try again.",
        )

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
        raise FormServiceError(
            "setup",
            f"Form setup failed when setting up CDS Entry Forms for students for cohort {cohort_no}. \nPlease restart the program and try again.",
        )

    email_result = input_email(
        "Enter an email address to share the form with: ",
    )
    if email_result.is_err():
        return
    recipient_email: str = email_result.unwrap()
    cds_form = run_share_form(cds_form, recipient_email)
    if cds_form is None:
        raise FormServiceError(
            "share",
            f"Form sharing failed when sharing the form with {recipient_email} \nPlease restart the program and try again.",
        )

    info: CDSFormInfo = CDSFormInfo(
        name=cds_form.name,
        title=cds_form.title,
        url=cds_form.url,
        uuid=cds_form.uuid,
        timestamp=timestamp,
    )
    history.add_cds_form(info)
    cds_form_path: Path = paths.get_cds_path("form", info.timestamp)
    with open(cds_form_path, "w") as json_file:
        json.dump(info.model_dump(), cast(TextIOWrapper, json_file), indent=2)
