from ..cli import input_email
from ..constants import COHORT
from ..data import DataStore
from ..errors import Result, Unit, eprint
from ..form_utils import (
    new_complaint_form,
    return_name,
)
from ..models import ContentBody, Form
from ..service import (
    run_create_form,
    run_publish_form,
    run_setup_form,
    run_share_form,
)


def init_complaint_form(ds: DataStore) -> Result[Unit]:
    cohort: int = ds.as_ref()[COHORT].tolist()[0]
    head = return_name(cohort, "Complaint")
    form_title, form_name = head.title, head.name
    form: Form | None = run_create_form(form_title, form_name)

    if form is None:
        msg = "Form creation failed when creating complaint form. Please try again."
        eprint(msg)
        return Result.err(msg)

    content_body: ContentBody = new_complaint_form(ds)
    form = run_setup_form(form, content_body)

    if form is None:
        msg = "Form setup failed when setting up complaint form. Please try again."
        eprint(msg)
        return Result.err(msg)

    form = run_publish_form(form)

    if form is None:
        msg = "Failed to publish form. Please try again."
        eprint(msg)
        return Result.err(msg)

    email_result = input_email("Enter an email address to share the form with: ")
    if email_result.is_err():
        return email_result.propagate()

    email: str = email_result.unwrap()

    form = run_share_form(form, email)

    if form is None:
        msg = "Form sharing failed when sharing complaint form. Please try again."
        eprint(msg)
        return Result.err(msg)

    return Result.unit()


def request_complaint_form(ds: DataStore) -> Result[Unit]:
    return init_complaint_form(ds)
