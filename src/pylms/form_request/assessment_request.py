from ..cli import input_option, input_str, provide_emails
from ..constants import COHORT, EMAIL, NAME
from ..data import DataStore
from ..errors import Result, Unit, eprint
from ..form_utils import new_assessment_content, return_name
from ..models import ContentBody, Form
from ..paths import must_get_env
from ..service import run_create_form, run_publish_form, run_setup_form, run_share_form


def init_assessment_form(ds: DataStore) -> Result[Unit]:
    options: list[str] = [
        "Midterm Assessment",
        "Final Assessment",
    ]
    option_result = input_option(options, prompt="Select the assessment type")
    if option_result.is_err():
        return option_result.propagate()
    _, assessment_type = option_result.unwrap()
    id_result = input_str("Enter the Assessment ID: ", lower_case=False)
    if id_result.is_err():
        return id_result.propagate()
    assessment_id: str = id_result.unwrap()
    names: list[str] = ds.pretty()[NAME].tolist()
    emails: list[str] = ds.pretty()[EMAIL].tolist()
    emails.sort()
    cohort: int = ds.as_ref()[COHORT].tolist()[0]

    head = return_name(cohort, f"{assessment_type} {assessment_id}")
    form_title, form_name = head.title, head.name
    form: Form | None = run_create_form(form_title, form_name)

    if form is None:
        msg = "Form creation failed. Please try again."
        eprint(msg)
        return Result.err(msg)

    content_body: ContentBody = new_assessment_content(names, emails)
    form = run_setup_form(form, content_body)

    if form is None:
        msg = "Form setup failed. Please try again."
        eprint(msg)
        return Result.err(msg)

    form = run_publish_form(form)

    if form is None:
        msg = "Failed to publish form. Please try again."
        eprint(msg)
        return Result.err(msg)

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
        msg = f"Form sharing failed. for emails = {msg} \nPlease try again."
        eprint(msg)
        return Result.err(msg)

    return Result.unit()


def request_assessment_form(ds: DataStore) -> Result[Unit]:
    return init_assessment_form(ds)
