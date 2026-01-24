from ..cli import input_email
from ..constants import COHORT
from ..data import DataStore
from ..errors import Result, Unit, eprint
from ..form_utils import (
    new_complaint_form,
    return_name,
)
from ..models import ContentBody
from ..service import (
    run_create_form,
    run_publish_form,
    run_setup_form,
    run_share_form,
)


def init_complaint_form(ds: DataStore) -> Result[Unit]:
    """Initialize complaint form for student feedback.
    
    Creates, sets up, publishes, and shares a complaint form for the cohort.
    
    Args:
        ds (DataStore): DataStore containing student data.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    cohort: int = ds.as_ref()[0, COHORT]
    head = return_name(cohort, "Complaint")
    form_title, form_name = head.title, head.name
    
    # Create form
    form = run_create_form(form_title, form_name)
    if form is None:
        msg = "Form creation failed when creating complaint form. Please try again."
        eprint(msg)
        return Result.err(msg)

    # Setup form content
    content_body: ContentBody = new_complaint_form(ds)
    form = run_setup_form(form, content_body)
    if form is None:
        msg = "Form setup failed when setting up complaint form. Please try again."
        eprint(msg)
        return Result.err(msg)

    # Publish form
    form = run_publish_form(form)
    if form is None:
        msg = "Failed to publish form. Please try again."
        eprint(msg)
        return Result.err(msg)

    # Share form with specified email
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
    """Request creation of complaint form.
    
    Args:
        ds (DataStore): DataStore containing student data.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    return init_complaint_form(ds)
