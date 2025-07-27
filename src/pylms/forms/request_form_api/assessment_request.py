from pylms.forms.utils import run_create_form, run_setup_form, run_share_form
from pylms.forms.request_form_api.errors import FormServiceError
from pylms.models import Form, ContentBody
from pylms.forms.request_form_api.utils.assessment_form_content import new_content_body
from pylms.utils import DataStore
from pylms.cli import input_email, input_option, input_str
from pylms.constants import NAME, COHORT, TIMESTAMP_FMT
from datetime import datetime


def init_assessment_form(ds: DataStore) -> None:
    options = [
        "Midterm Assessment",
        "Final Assessment",
    ]
    _, assessment_type = input_option(options, prompt="Select the assessment type")
    assessment_id: str = input_str("Enter the Assessment ID: ", lower_case=False)
    timestamp: str = datetime.now().strftime(TIMESTAMP_FMT)
    names: list[str] = ds.pretty()[NAME].tolist()
    cohort: int = ds.as_ref()[COHORT].tolist()[0]
    form_title: str = (
        f"Python Beginners Cohort {cohort} {assessment_type} {assessment_id}"
    )
    form_name: str = f"Cohort {cohort} {assessment_type} {assessment_id} {timestamp}"
    form: Form | None = run_create_form(form_title, form_name)

    if form is None:
        raise FormServiceError("create", "Form creation failed. \nPlease try again.")

    content_body: ContentBody = new_content_body(names)
    form = run_setup_form(form, content_body)

    if form is None:
        raise FormServiceError("setup", "Form setup failed. \nPlease try again.")

    email: str = input_email("Enter an email address to share the form with: ")

    form = run_share_form(form, email)

    if form is None:
        raise FormServiceError("share", "Form sharing failed. \nPlease try again.")


def request_assessment_form(ds: DataStore) -> None:
    init_assessment_form(ds)
