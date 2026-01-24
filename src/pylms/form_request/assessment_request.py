from ..cli import input_option, input_str, provide_emails
from ..constants import COHORT, EMAIL, NAME
from ..data import DataStore
from ..errors import Result, Unit, eprint
from ..form_utils import new_assessment_content, return_name
from ..models import ContentBody, Form
from ..paths import must_get_env
from ..service import run_create_form, run_publish_form, run_setup_form, run_share_form


def init_assessment_form(ds: DataStore) -> Result[Unit]:
    """Initialize and create assessment form for students.
    
    Args:
        ds (DataStore): DataStore containing student data.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    options: list[str] = [
        "Midterm Assessment",
        "Final Assessment",
    ]
    option = input_option(options, prompt="Select the assessment type")
    if option.is_err():
        return option.propagate()
    _, assessment_type = option.unwrap()
    
    assessment_id = input_str("Enter the Assessment ID: ", lower_case=False)
    if assessment_id.is_err():
        return assessment_id.propagate()
    assessment_id = assessment_id.unwrap()

    # Extract student data
    pretty = ds.pretty()
    names: list[str] = pretty[NAME].to_list()
    emails: list[str] = pretty[EMAIL].to_list()
    emails.sort()
    cohort: int = pretty[0, COHORT]

    # Create form with title and name
    head = return_name(cohort, f"{assessment_type} {assessment_id}")
    form_title, form_name = head.title, head.name
    form: Form | None = run_create_form(form_title, form_name)

    if form is None:
        msg = "Form creation failed. Please try again."
        eprint(msg)
        return Result.err(msg)

    # Setup form content
    content_body: ContentBody = new_assessment_content(names, emails)
    form = run_setup_form(form, content_body)

    if form is None:
        msg = "Form setup failed. Please try again."
        eprint(msg)
        return Result.err(msg)

    # Publish form
    form = run_publish_form(form)

    if form is None:
        msg = "Failed to publish form. Please try again."
        eprint(msg)
        return Result.err(msg)

    # Share form with specified emails
    share_to_emails = provide_emails()
    email_default: str = must_get_env("EMAIL")
    share_to_emails = share_to_emails.unwrap_or([email_default])

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
    """Request creation of assessment form.
    
    Args:
        ds (DataStore): DataStore containing student data.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    return init_assessment_form(ds)
