from ..cli import input_option, input_str
from ..config import Config
from ..constants import COHORT, EMAIL, NAME
from ..data import DataStore
from ..errors import Result, Unit
from ..form_utils import new_assessment_content, return_name
from ..models import ContentBody
from ..service import (
    run_create_form,
    run_publish_form,
    run_setup_form,
    run_share_form_multiple,
)


def init_assessment_form(config: Config, ds: DataStore) -> Result[Unit]:
    """Initialize and create assessment form for students.

    Args:
        config (Config): Config containing facilitator information.
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
    form_result = run_create_form(form_title, form_name)
    if form_result.is_err():
        return form_result.propagate()
    form = form_result.unwrap()

    # Setup form content
    content_body: ContentBody = new_assessment_content(names, emails)
    form_result = run_setup_form(form, content_body)
    if form_result.is_err():
        return form_result.propagate()
    form = form_result.unwrap()

    # Publish form
    form_result = run_publish_form(form)
    if form_result.is_err():
        return form_result.propagate()
    form = form_result.unwrap()

    # Share form with facilitators
    gmails: list[str] = [f.gmail for f in config.facilitators]
    form_result = run_share_form_multiple(form, gmails)
    if form_result.is_err():
        return form_result.propagate()

    return Result.unit()


def request_assessment_form(config: Config, ds: DataStore) -> Result[Unit]:
    """Request creation of assessment form.

    Args:
        config (Config): Config containing facilitator information.
        ds (DataStore): DataStore containing student data.

    Returns:
        Result[Unit]: Success or error message.
    """
    return init_assessment_form(config, ds)
