from datetime import datetime

from pylms.cli import input_option, input_str
from pylms.cli.emails_input import provide_emails
from pylms.constants import COHORT, EMAIL, NAME, TIMESTAMP_FMT
from pylms.errors import Result
from pylms.forms.request_form_api.errors import FormServiceError
from pylms.forms.request_form_api.utils.assessment_form_content import new_content_body
from pylms.forms.utils import run_create_form, run_setup_form, run_share_form
from pylms.models import ContentBody, Form
from pylms.utils import DataStore
from pylms.utils.env import must_get_env


def init_assessment_form(ds: DataStore) -> None:
    options: list[str] = [
        "Midterm Assessment",
        "Final Assessment",
    ]
    option_result = input_option(options, prompt="Select the assessment type")
    if option_result.is_err():
        return
    _, assessment_type = option_result.unwrap()
    id_result = input_str("Enter the Assessment ID: ", lower_case=False)
    if id_result.is_err():
        return None
    assessment_id: str = id_result.unwrap()
    timestamp: str = datetime.now().strftime(TIMESTAMP_FMT)
    names: list[str] = ds.pretty()[NAME].tolist()
    emails: list[str] = ds.pretty()[EMAIL].tolist()
    emails.sort()
    cohort: int = ds.as_ref()[COHORT].tolist()[0]
    form_title: str = (
        f"Python Beginners Cohort {cohort} {assessment_type} {assessment_id}"
    )
    form_name: str = f"Cohort {cohort} {assessment_type} {assessment_id} {timestamp}"
    form: Form | None = run_create_form(form_title, form_name)

    if form is None:
        raise FormServiceError("create", "Form creation failed. \nPlease try again.")

    content_body: ContentBody = new_content_body(names, emails)
    form = run_setup_form(form, content_body)

    if form is None:
        raise FormServiceError("setup", "Form setup failed. \nPlease try again.")

    email_result: Result[list[str]] = provide_emails()

    email_default: str = must_get_env("EMAIL")

    share_to_emails: list[str] = email_result.unwrap_or([email_default])

    failed_emails: list[str] = []

    for email in share_to_emails:
        success_form: Form | None = run_share_form(form, email)

        if success_form is None:
            failed_emails.append(email)

    if len(failed_emails) > 0:
        failed_emails_print: list[str] = [
            f"{i}. {email}" for (i, email) in enumerate(failed_emails, start=1)
        ]
        msg = f"""[
    {"\n".join(failed_emails_print)}
]"""
        raise FormServiceError(
            "share", f"Form sharing failed. for emails = {msg} \nPlease try again."
        )


def request_assessment_form(ds: DataStore) -> None:
    init_assessment_form(ds)
