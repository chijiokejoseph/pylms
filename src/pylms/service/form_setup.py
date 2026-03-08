from typing import Any

from googleapiclient.http import HttpRequest  # pyright: ignore[reportMissingTypeStubs]

from ..cli_utils import emphasis
from ..errors import Result, eprint
from ..info import print_info
from ..models import ContentBody, Form
from ._resource import FormResource, FormsService
from .service_init import run_service


def _setup_form(
    form: Form, form_content: ContentBody, *, service: FormsService
) -> Result[Form]:
    """Completes form initialization by adding questions and content.
    
    Updates a partially initialized form with questions, descriptions, and other
    content using the Google Forms API batchUpdate method.
    
    Args:
        form: Partially initialized Form object from run_create_form.
        form_content: ContentBody containing questions and form structure.
        service: FormsService object for API calls.
        
    Returns:
        Result[Form]: The same Form object on success, error otherwise.
    """
    # Extract form ID and prepare update request
    form_id: str = form.uuid
    form_resource: FormResource = service.forms()
    request_body: dict[str, Any] = form_content.model_dump(exclude_none=True)
    
    try:
        # Batch update form with content
        request: HttpRequest = form_resource.batchUpdate(
            formId=form_id, body=request_body
        )
        request.execute()  # pyright: ignore [reportUnknownMemberType]
        print_info(
            f"Form with \nName = {emphasis(form.name)}\nTitle = {emphasis(form.title)}\nUrl = {emphasis(form.url)}"
        )
        print_info("Setup successfully.\n")
        return Result.ok(form)
    except Exception as e:
        msg = f"Fatal error occurred while updating form. Error encountered is {e}\n"
        eprint(msg)
        return Result.err(msg)


def run_setup_form(form: Form, form_content: ContentBody) -> Result[Form]:
    """Completes form initialization by adding questions and content.
    
    Updates a partially initialized form from run_create_form with questions,
    descriptions, and other content. The ContentBody structure contains a list
    of Content items representing form questions and elements.
    
    Args:
        form: Partially initialized Form object from run_create_form.
        form_content: ContentBody containing questions and form structure.
        
    Returns:
        Result[Form]: The same Form object on success, error otherwise.
    """
    # Wrapper to inject FormsService dependency
    def _run_service(service: FormsService) -> Result[Form]:
        return _setup_form(form, form_content, service=service)

    return run_service(
        api="forms",
        version="v1",
        func=_run_service,
    )
