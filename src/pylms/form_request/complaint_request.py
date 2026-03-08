from ..config import Config
from ..constants import COHORT
from ..data import DataStore
from ..errors import Result, Unit
from ..form_utils import (
    new_complaint_form,
    return_name,
)
from ..models import ContentBody
from ..service import (
    run_create_form,
    run_publish_form,
    run_setup_form,
    run_share_form_multiple,
)
from .share_emails import input_share_emails


def init_complaint_form(config: Config, ds: DataStore) -> Result[Unit]:
    """Initialize complaint form for student feedback.
    
    Args:
        config: Config containing admin and facilitator information.
        ds: DataStore containing student data.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    cohort: int = ds.as_ref()[0, COHORT]
    head = return_name(cohort, "Complaint")
    form_title, form_name = head.title, head.name
    
    # Create form
    form_result = run_create_form(form_title, form_name)
    if form_result.is_err():
        return form_result.propagate()
    form = form_result.unwrap()

    # Setup form content
    content_body: ContentBody = new_complaint_form(ds)
    form_result = run_setup_form(form, content_body)
    if form_result.is_err():
        return form_result.propagate()
    form = form_result.unwrap()

    # Publish form
    form_result = run_publish_form(form)
    if form_result.is_err():
        return form_result.propagate()
    form = form_result.unwrap()

    # Get emails to share with
    gmails_result = input_share_emails(config)
    if gmails_result.is_err():
        return gmails_result.propagate()
    gmails = gmails_result.unwrap()

    # Share form
    form_result = run_share_form_multiple(form, gmails)
    if form_result.is_err():
        return form_result.propagate()

    return Result.unit()


def request_complaint_form(config: Config, ds: DataStore) -> Result[Unit]:
    """Request creation of complaint form.
    
    Args:
        config: Config containing admin and facilitator information.
        ds: DataStore containing student data.
        
    Returns:
        Result[Unit]: Success or error message.
    """
    return init_complaint_form(config, ds)
