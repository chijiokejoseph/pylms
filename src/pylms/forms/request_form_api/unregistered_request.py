from pylms.forms.utils import (
    run_create_form,
    run_setup_form,
    run_share_form,
)
from pylms.forms.request_form_api.errors import FormServiceError
from pylms.models import Form, ContentBody
from pylms.forms.request_form_api.utils.unregistered_form_content import (
    new_content_body,
)
from pylms.cli import input_email
from pylms.utils import DataStore
from pylms.constants import COHORT, TIMESTAMP_FMT
from datetime import datetime


def init_unregistered_form(ds: DataStore) -> None:
    timestamp: str = datetime.now().strftime(TIMESTAMP_FMT)
    cohort: int = ds.as_ref()[COHORT].tolist()[0]
    form_title: str = f"Python Beginners Cohort {cohort} Unregistered Form"
    form_name: str = f"Cohort {cohort} Unregistered Form {timestamp}"
    form: Form | None = run_create_form(form_title, form_name)

    if form is None:
        raise FormServiceError(
            "create",
            "Form creation failed when creating unregistered entry form. \nPlease try again.",
        )

    content_body: ContentBody = new_content_body()
    form = run_setup_form(form, content_body)

    if form is None:
        raise FormServiceError(
            "setup",
            "Form setup failed when setting up unregistered entry form. \nPlease try again.",
        )

    email: str = input_email("Enter an email address to share the form with: ")

    form = run_share_form(form, email)

    if form is None:
        raise FormServiceError(
            "share",
            "Form sharing failed when sharing unregistered entry form. \nPlease try again.",
        )
        
        
def request_unregistered_form(ds: DataStore) -> None:
    init_unregistered_form(ds)
